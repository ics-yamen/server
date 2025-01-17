import json

from typing import List, Union
from django.contrib.gis.db import models
from django.core.serializers import serialize
from django.db import transaction, connection
from django.contrib.gis.gdal import Envelope
from django.contrib.gis.db.models.aggregates import Union as PgUnion
from django.contrib.gis.db.models.functions import Centroid

from utils.files import generate_json_file_for_upload
from user_resource.models import UserResource
from gallery.models import File


class Region(UserResource):
    """
    Region model

    Represents mostly country but can also be any other region.
    Region can be global in which case it will be available directly
    to public. Project specific regions won't be available publicly.
    """
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    public = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    regional_groups = models.JSONField(default=None, blank=True, null=True)
    key_figures = models.JSONField(default=None, blank=True, null=True)
    population_data = models.JSONField(default=None, blank=True, null=True)
    media_sources = models.JSONField(default=None, blank=True, null=True)

    # cache data
    cache_index = models.SmallIntegerField(default=0)  # Used to track cache update.
    centroid = models.PointField(blank=True, null=True)  # Admin level 0 centroid
    geo_options = models.JSONField(default=None, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        self.id: Union[int, None]
        self.adminlevel_set: models.QuerySet[AdminLevel]
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"[{'Public' if self.public else 'Private'}] {self.title}"

    class Meta:
        ordering = ['title', 'code']

    def calc_cache(self, save=True):
        self.geo_options = [
            {
                'label': '{} / {}'.format(geo_area.admin_level.title, geo_area.title),
                'title': geo_area.title,
                'key': str(geo_area.id),
                'admin_level': geo_area.admin_level.level,
                'admin_level_title': geo_area.admin_level.title,
                'region': self.id,
                'region_title': self.title,
                'parent': geo_area.parent.id if geo_area.parent else None,
            } for geo_area in GeoArea.objects.prefetch_related(
                'admin_level',
            ).filter(
                admin_level__region=self
            ).order_by('admin_level__level').distinct()
        ]

        # Calculate region centroid
        self.centroid = GeoArea.objects\
            .filter(admin_level__region=self)\
            .aggregate(centroid=Centroid(PgUnion(Centroid('polygons'))))['centroid']
        self.cache_index += 1  # Increment after every calc_cache. This is used by project to generate overall cache.
        if save:
            self.save()

    def get_verbose_title(self):
        if self.public:
            return self.title
        return '{} (Private)'.format(self.title)

    def clone_to_private(self, user):
        region = Region(
            code=self.code,
            # Strip off extra chars from title to add ' (cloned)
            title='{} (cloned)'.format(self.title[:230]),
            public=False,
            regional_groups=self.regional_groups,
            key_figures=self.key_figures,
            population_data=self.population_data,
            media_sources=self.media_sources,
        )

        region.created_by = user
        region.modified_by = user
        region.save()

        root_levels = AdminLevel.objects.filter(
            region=self,
            parent=None,
        ).distinct()

        for root_level in root_levels:
            root_level.clone_to(region)

        return region

    @staticmethod
    def get_for(user):
        return Region.objects.filter(
            models.Q(public=True) |
            models.Q(created_by=user) |
            models.Q(project__members=user)
        ).distinct()

    def can_get(self, user):
        return self in Region.get_for(user)

    def can_modify(self, user):
        from project.models import ProjectMembership, ProjectRole
        return (
            # Either created by user
            not self.is_published and (
                (self.created_by == user) or
                # Or is public and user is superuser
                (self.public and user.is_superuser) or
                # Or is private and user is admin of one of the projects
                # with this region
                (not self.public and ProjectMembership.objects.filter(
                    project__regions=self,
                    member=user,
                    role__in=ProjectRole.get_admin_roles(),
                ).exists())
            )
        )

    def can_publish(self, user):
        return user == self.created_by


class AdminLevel(models.Model):
    """
    A region can contain multiple admin levels.

    Admin level data is in the form of geojson.

    Note that to auto generate geo areas from geojson
    we need (at least some of) the following attributes:

    * name_prop -   Property defining name of geo area
    * code_prop -   Property defining code of geo area

    To also auto link parent geo areas:

    * parent_name_prop  -   Property defining name of parent of the geo area
    * parent_code_prop  -   Property defining code of parent of the geo area
    """
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    parent = models.ForeignKey('AdminLevel',
                               on_delete=models.SET_NULL,
                               null=True, blank=True, default=None)
    title = models.CharField(max_length=255)
    level = models.IntegerField(null=True, blank=True, default=None)
    name_prop = models.CharField(max_length=255, blank=True)
    code_prop = models.CharField(max_length=255, blank=True)
    parent_name_prop = models.CharField(max_length=255, blank=True)
    parent_code_prop = models.CharField(max_length=255, blank=True)

    geo_shape_file = models.ForeignKey(File, on_delete=models.SET_NULL,
                                       null=True, blank=True, default=None)
    tolerance = models.FloatField(default=0.0001)

    stale_geo_areas = models.BooleanField(default=True)

    # cache data
    geojson_file = models.FileField(
        upload_to='geojson/', max_length=255, null=True, blank=True, default=None,
    )
    bounds_file = models.FileField(
        upload_to='geo-bounds/', max_length=255, null=True, blank=True, default=None,
    )
    geo_area_titles = models.JSONField(default=None, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['level']

    def get_geo_area_titles(self):
        if not self.geo_area_titles:
            self.calc_cache()
        return self.geo_area_titles

    def calc_cache(self, save=True):
        # Update geo parent_titles data
        with transaction.atomic():
            GEO_PARENT_DATA_CALC_SQL = f'''
                WITH geo_parents_data as (
                  SELECT
                    id,
                    title,
                    (
                      WITH RECURSIVE parents AS (
                       SELECT
                        sub_g.id,
                        sub_g.title,
                        sub_g.parent_id,
                        sub_g.admin_level_id,
                        sub_adminlevel.level
                       FROM {GeoArea._meta.db_table} sub_g
                         INNER JOIN {AdminLevel._meta.db_table} AS sub_adminlevel
                            ON sub_adminlevel.id = sub_g.admin_level_id
                       WHERE sub_g.id = outer_g.parent_id
                       UNION
                       SELECT
                        sub_parent_g.id,
                        sub_parent_g.title,
                        sub_parent_g.parent_id,
                        sub_parent_g.admin_level_id,
                        sub_parent_adminlevel.level
                       FROM {GeoArea._meta.db_table} AS sub_parent_g
                         INNER JOIN parents ON sub_parent_g.id = parents.parent_id
                         INNER JOIN {AdminLevel._meta.db_table} AS sub_parent_adminlevel
                            ON sub_parent_adminlevel.id = sub_parent_g.admin_level_id
                      ) SELECT array_agg(title ORDER BY level) from parents
                    ) as parent_titles
                  FROM {GeoArea._meta.db_table} as outer_g
                  WHERE admin_level_id = %(admin_level_id)s
                )
                UPDATE {GeoArea._meta.db_table} AS G
                SET
                    cached_data = JSONB_SET(
                        COALESCE(G.cached_data, '{{}}'),
                        '{{parent_titles}}',
                        TO_JSONB(GP.parent_titles), true
                    )
                FROM geo_parents_data GP
                WHERE
                    G.id = GP.id
            '''
            with connection.cursor() as cursor:
                cursor.execute(GEO_PARENT_DATA_CALC_SQL, {'admin_level_id': self.pk})

        geojson = json.loads(serialize(
            'geojson',
            self.geoarea_set.all(),
            geometry_field='polygons',
            fields=('pk', 'title', 'code', 'cached_data'),
        ))

        # Titles
        titles = {}
        for geo_area in self.geoarea_set.all():
            titles[str(geo_area.id)] = {
                'title': geo_area.title,
                'parent_id': str(geo_area.parent.pk) if geo_area.parent else None,
                'code': geo_area.code,
            }
        self.geo_area_titles = titles

        # Bounds
        bounds = {}
        areas = self.geoarea_set.filter(polygons__isnull=False)
        if areas.count() > 0:
            try:
                envelope = Envelope(*areas[0].polygons.extent)
                for area in areas[1:]:
                    envelope.expand_to_include(*area.polygons.extent)
                bounds = {
                    'minX': envelope.min_x,
                    'minY': envelope.min_y,
                    'maxX': envelope.max_x,
                    'maxY': envelope.max_y,
                }
            except ValueError:
                pass

        self.geojson_file.save(
            f'admin-level-{self.pk}.json',
            generate_json_file_for_upload(geojson),
        )
        self.bounds_file.save(
            f'admin-level-{self.pk}.json',
            generate_json_file_for_upload({'bounds': bounds}),
        )
        if save:
            self.save()

    def clone_to(self, region, parent=None):
        admin_level = AdminLevel(
            region=region,
            parent=parent,
            title=self.title,
            level=self.level,
            name_prop=self.name_prop,
            code_prop=self.code_prop,
            parent_name_prop=self.parent_name_prop,
            parent_code_prop=self.parent_code_prop,
            geo_shape_file=self.geo_shape_file,
            tolerance=self.tolerance,
            geojson_file=self.geojson_file,
            bounds_file=self.bounds_file,
            geo_area_titles=self.geo_area_titles,
        )
        admin_level.stale_geo_areas = True
        admin_level.save()

        for child_level in self.adminlevel_set.all():
            child_level.clone_to(region, admin_level)

        for geoarea in self.geoarea_set.all():
            geoarea.clone_to(admin_level)

        return admin_level

    # Admin level permissions are same as region permissions

    @staticmethod
    def get_for(user):
        return AdminLevel.objects.filter(
            models.Q(region__public=True) |
            models.Q(region__created_by=user) |
            models.Q(region__project__members=user)
        ).distinct()

    def can_get(self, user):
        return self.region.can_get(user)

    def can_modify(self, user):
        return self.region.can_modify(user)


class GeoArea(models.Model):
    """
    An actual geo area in a given admin level
    """
    admin_level = models.ForeignKey(AdminLevel, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'GeoArea',
        on_delete=models.SET_NULL,
        null=True, blank=True, default=None,
    )
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255, blank=True)

    # TODO Rename to geometry
    polygons = models.GeometryField(null=True, blank=True, default=None)

    # Cache
    centroid = models.PointField(blank=True, null=True)
    # -- Used to store additional data
    cached_data = models.JSONField(default=None, blank=True, null=True)

    def __str__(self):
        return self.title

    @classmethod
    def sync_centroid(cls):
        cls.objects.filter(
            (
                models.Q(centroid__isempty=True) |
                models.Q(centroid__isnull=True)
            ),
            polygons__isempty=False,
        ).update(
            centroid=Centroid('polygons')
        )

    @classmethod
    def get_for_project(cls, project, is_published=True):
        admin_levels_qs = AdminLevel.objects.filter(
            region__is_published=is_published,
            region__project=project,
        )
        return cls.objects.filter(admin_level__in=admin_levels_qs)

    def clone_to(self, admin_level, parent=None):
        geo_area = GeoArea(
            admin_level=admin_level,
            parent=parent,
            # Strip off extra chars from title to add ' (cloned)
            title='{} (cloned)'.format(self.title[:230]),
            code=self.code,
            data=self.data,
            polygons=self.polygons,
        )
        geo_area.save()

        for child_geoarea in self.geoarea_set.all():
            child_geoarea.clone_to(admin_level, geo_area)

        return geo_area

    @classmethod
    def get_sub_childrens(cls, value: List[Union[str, int]], level=1):
        if value:
            filters = models.Q(id__in=list(value))
            for i in range(level - 1):
                filters |= models.Q(**{f"{'parent__' * i}parent__in": value})
            return cls.objects.filter(filters)
        return cls.objects.none()

    # Permissions are same as region
    @staticmethod
    def get_for(user):
        return AdminLevel.objects.filter(
            models.Q(admin_level__region__public=True) |
            models.Q(admin_level__region__created_by=user) |
            models.Q(admin_level__region__project__members=user)
        ).distinct()

    def can_get(self, user):
        return self.admin_level.can_get(user)

    def can_modify(self, user):
        return self.admin_level.can_modify(user)

    def get_label(self):
        return '{} / {}'.format(self.admin_level.title, self.title)
