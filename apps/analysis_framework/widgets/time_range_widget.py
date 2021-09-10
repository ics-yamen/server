WIDGET_ID = 'timeRangeWidget'


def get_filters(widget, data):
    from analysis_framework.models import Filter  # To avoid circular import

    return [{
        'filter_type': Filter.FilterType.INTERSECTS,
        'properties': {
            'type': 'time',
        },
    }]


def get_exportable(widget, data):
    return {
        'excel': {
            'type': 'multiple',
            'titles': [
                '{} (From)'.format(widget.title),
                '{} (To)'.format(widget.title),
            ],
            'col_type': [
                'time',
                'time',
            ],
        },
    }
