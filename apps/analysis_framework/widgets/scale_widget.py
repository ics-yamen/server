WIDGET_ID = 'scaleWidget'


"""
properties:
    defaultValue?: string
    options: [
        key: string
        label: string
        tooltip?: string
        order: number
        color: string
    ]
"""


def get_filters(widget, properties):
    from analysis_framework.models import Filter  # To avoid circular import

    filter_options = [
        {
            'key': option['key'],
            'label': option['label'],
        } for option in properties.get('options', [])
    ]
    return [{
        'filter_type': Filter.FilterType.LIST,
        'properties': {
            'type': 'multiselect-range',
            'options': filter_options
        },
    }]


def get_exportable(widget, data):
    return {
        'excel': {
            'title': widget.title,
        },
    }
