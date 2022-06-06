import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField
from django.db.models import Prefetch

from utils.graphene.enums import EnumDescription
from user_resource.schema import UserResourceMixin
from deep.permissions import ProjectPermissions as PP

from geo.schema import (
    ProjectGeoAreaType,
    get_geo_area_queryset_for_project_geo_area_type,
)
from .models import (
    DraftEntry,
    AssistedTaggingModel,
    AssistedTaggingModelVersion,
    AssistedTaggingModelPredictionTag,
    AssistedTaggingPrediction,
    MissingPredictionReview,
    WrongPredictionReview,
)
from .enums import (
    DraftEntryPredictionStatusEnum,
    AssistedTaggingPredictionDataTypeEnum,
)


# -- Global Level
class AssistedTaggingModelVersionType(DjangoObjectType):
    class Meta:
        model = AssistedTaggingModelVersion
        only_fields = (
            'id',
            'version',
        )


class AssistedTaggingModelType(DjangoObjectType):
    versions = graphene.List(
        graphene.NonNull(AssistedTaggingModelVersionType)
    )

    class Meta:
        model = AssistedTaggingModel
        only_fields = (
            'id',
            'name',
            'model_id',
        )

    @staticmethod
    def resolve_versions(root, info, **kwargs):
        return root.versions.all()   # NOTE: Prefetched


class AssistedTaggingModelPredictionTagType(DjangoObjectType):
    parent_tag = graphene.ID(source='parent_tag_id')

    class Meta:
        model = AssistedTaggingModelPredictionTag
        only_fields = (
            'id',
            'name',
            'group',
            'tag_id',
            'is_category',
            'is_deprecated',
            'hide_in_analysis_framework_mapping',
        )


class AssistedTaggingRootQueryType(graphene.ObjectType):
    tagging_model = DjangoObjectField(AssistedTaggingModelType)
    tagging_models = graphene.List(
        graphene.NonNull(AssistedTaggingModelType),
    )

    prediction_tag = DjangoObjectField(AssistedTaggingModelPredictionTagType)
    prediction_tags = graphene.List(
        graphene.NonNull(AssistedTaggingModelPredictionTagType)
    )

    @staticmethod
    def resolve_tagging_models(root, info, **kwargs):
        return AssistedTaggingModel.objects.prefetch_related(
            Prefetch(
                'versions',
                queryset=AssistedTaggingModelVersion.objects.order_by('-version'),
            ),
        ).all()

    @staticmethod
    def resolve_prediction_tags(root, info, **kwargs):
        return AssistedTaggingModelPredictionTag.objects.all()


# -- Project Level
def get_draft_entry_qs(info):
    qs = DraftEntry.objects.filter(project=info.context.active_project)
    if PP.check_permission(info, PP.Permission.VIEW_ENTRY):
        return qs
    return qs.none()


class WrongPredictionReviewType(UserResourceMixin, DjangoObjectType):
    prediction = graphene.ID(source='prediction_id', required=True)

    class Meta:
        model = WrongPredictionReview
        only_fields = (
            'id',
        )


class AssistedTaggingPredictionType(DjangoObjectType):
    model_version = graphene.ID(source='model_version_id', required=True)
    model_version_deepl_model_id = graphene.String(required=True)
    draft_entry = graphene.ID(source='draft_entry_id', required=True)
    data_type = graphene.Field(AssistedTaggingPredictionDataTypeEnum, required=True)
    data_type_display = EnumDescription(source='get_data_type_display', required=True)
    category = graphene.ID(source='category_id')
    tag = graphene.ID(source='tag_id')
    wrong_prediction_reviews = graphene.List(
        graphene.NonNull(WrongPredictionReviewType),
    )

    class Meta:
        model = AssistedTaggingPrediction
        only_fields = (
            'id',
            'value',
            'prediction',
            'threshold',
            'is_selected',
        )

    @staticmethod
    def resolve_wrong_prediction_reviews(root, info, **kwargs):
        return root.wrong_prediction_reviews.all()   # NOTE: Prefetched by DraftEntry

    @staticmethod
    def resolve_model_version_deepl_model_id(root, info, **kwargs):
        return root.model_version.model.model_id   # NOTE: Prefetched by DraftEntry


class MissingPredictionReviewType(UserResourceMixin, DjangoObjectType):
    category = graphene.ID(source='category_id', required=True)
    tag = graphene.ID(source='tag_id', required=True)
    draft_entry = graphene.ID(source='draft_entry_id', required=True)

    class Meta:
        model = MissingPredictionReview
        only_fields = (
            'id',
        )


class DraftEntryType(DjangoObjectType):
    prediction_status = graphene.Field(DraftEntryPredictionStatusEnum, required=True)
    prediction_status_display = EnumDescription(source='get_prediction_status_display', required=True)
    predictions = graphene.List(
        graphene.NonNull(AssistedTaggingPredictionType)
    )
    missing_prediction_reviews = graphene.List(
        graphene.NonNull(MissingPredictionReviewType),
    )
    related_geoareas = graphene.List(
        graphene.NonNull(ProjectGeoAreaType)
    )

    class Meta:
        model = DraftEntry
        only_fields = (
            'id',
            'excerpt',
            'prediction_received_at',
        )

    @staticmethod
    def get_custom_queryset(queryset, info, **kwargs):
        return get_draft_entry_qs(info).prefetch_related(
            Prefetch(
                'predictions',
                queryset=AssistedTaggingPrediction.objects.order_by('id'),
            ),
            Prefetch(
                'related_geoareas',
                queryset=get_geo_area_queryset_for_project_geo_area_type().order_by('id'),
            ),
            'predictions__model_version',
            'predictions__model_version__model',
            'predictions__wrong_prediction_reviews',
            'missing_prediction_reviews',
            'related_geoareas',
        )

    @staticmethod
    def resolve_predictions(root, info, **kwargs):
        return root.predictions.all()   # NOTE: Prefetched by DraftEntry

    @staticmethod
    def resolve_missing_prediction_reviews(root, info, **kwargs):
        return root.missing_prediction_reviews.all()   # NOTE: Prefetched by DraftEntry

    @staticmethod
    def resolve_related_geoareas(root, info, **kwargs):
        return root.related_geoareas.all()   # NOTE: Prefetched by DraftEntry


# This is attached to project type.
class AssistedTaggingQueryType(graphene.ObjectType):
    draft_entry = DjangoObjectField(DraftEntryType)