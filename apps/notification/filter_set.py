import django_filters
from django.db.models import Q

from utils.graphene.filters import SimpleInputFilter
from .models import Notification, Assignment
from .enums import NotificationStatusEnum, NotificationTypeEnum


class NotificationFilterSet(django_filters.FilterSet):
    """
    Notification filter set
    """

    TRUE = 'true'
    FALSE = 'false'
    BOOLEAN_CHOICES = (
        (TRUE, 'True'),
        (FALSE, 'False'),
    )

    timestamp__lt = django_filters.DateFilter(
        field_name='timestamp', lookup_expr='lt',
        input_formats=['%Y-%m-%d%z'],
    )
    timestamp__gt = django_filters.DateFilter(
        field_name='timestamp', lookup_expr='gt',
        input_formats=['%Y-%m-%d%z'],
    )
    timestamp__lte = django_filters.DateFilter(
        field_name='timestamp', lookup_expr='lte',
        input_formats=['%Y-%m-%d%z'],
    )
    timestamp__gte = django_filters.DateFilter(
        field_name='timestamp', lookup_expr='gte',
        input_formats=['%Y-%m-%d%z'],
    )
    is_pending = django_filters.ChoiceFilter(
        label='Action Status',
        method='is_pending_filter',
        choices=BOOLEAN_CHOICES
    )

    class Meta:
        model = Notification
        fields = {
            'timestamp': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'status': ['exact'],
            'notification_type': ['exact'],
        }

    def is_pending_filter(self, queryset, name, value):
        if value == self.TRUE:
            return queryset.filter(
                data__status='pending',
            ).distinct()
        elif value == self.FALSE:
            return queryset.filter(
                ~Q(data__status='pending') | Q(data__status__isnull=True)
            ).distinct()
        return queryset


class AssignmentFilterSet(django_filters.FilterSet):
    class Meta:
        model = Assignment
        fields = ('project', 'is_done')


# -------------------- Graphql Filters -----------------------------------
class NotificationGqlFilterSet(django_filters.FilterSet):
    timestamp = django_filters.DateTimeFilter(
        field_name='timestamp',
        input_formats=[django_filters.fields.IsoDateTimeField.ISO_8601],
    )
    timestamp_lte = django_filters.DateTimeFilter(
        field_name='timestamp', lookup_expr='lte',
        input_formats=[django_filters.fields.IsoDateTimeField.ISO_8601],
    )
    timestamp_gte = django_filters.DateTimeFilter(
        field_name='timestamp', lookup_expr='gte',
        input_formats=[django_filters.fields.IsoDateTimeField.ISO_8601],
    )

    is_pending = django_filters.BooleanFilter(label='Action Status', method='is_pending_filter')
    notification_type = SimpleInputFilter(NotificationTypeEnum)
    status = SimpleInputFilter(NotificationStatusEnum)

    class Meta:
        model = Notification
        fields = ()

    def is_pending_filter(self, queryset, _, value):
        if value is True:
            return queryset.filter(
                data__status='pending',
            ).distinct()
        elif value is False:
            return queryset.filter(
                ~Q(data__status='pending') | Q(data__status__isnull=True)
            ).distinct()
        # If none
        return queryset
