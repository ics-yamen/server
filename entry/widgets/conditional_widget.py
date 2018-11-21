class Dummy:
    pass


def update_attribute(widget, data, widget_data):
    from entry.widgets.store import widget_store

    value = data.get('value', {})
    selected_widget_key = value.get('selected_widget_key')

    widgets = [
        w.get('widget')
        for w in (widget_data.get('widgets') or [])
    ]

    filter_data = []
    excel_data = []
    report_keys = []
    for w in widgets:
        widget_module = widget_store.get(w.get('widget_id'))
        if not widget_module:
            continue

        w_key = w.get('key')
        if w_key == selected_widget_key:
            w_data = value.get(w_key, {}).get('data', {})
        else:
            w_data = {}

        w_widget_data = w.get('properties', {}).get('data', {})

        w_obj = Dummy()
        w_obj.key = w_key

        update_info = widget_module.update_attribute(
            w_obj,
            w_data,
            w_widget_data,
        )
        w_filter_data = update_info.get('filter_data') or []
        w_export_data = update_info.get('export_data')

        filter_data = filter_data + [{
            **wfd,
            'key': '{}-{}'.format(
                widget.key,
                wfd.get('key', w_key),
            )
        } for wfd in w_filter_data]

        if w_export_data:
            excel_data.append(w_export_data.get('data', {}).get('excel'))
            report_keys += w_export_data.get('data', {})\
                .get('report', {})\
                .get('keys') or []
        else:
            excel_data.append(None)

    return {
        'filter_data': filter_data,
        'export_data': {
            'data': {
                'excel': excel_data,
                'report': {
                    'keys': report_keys,
                },
            },
        },
    }