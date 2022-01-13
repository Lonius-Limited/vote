frappe.views.calendar['Election'] = {
    field_map: {
        start: 'election_start',
        end: 'election_end',
        id: 'name',
        allDay: 'all_day',
        title: 'name',
        status: 'status',
        color: 'color'
    },
    style_map: {
        Public: 'success',
        Private: 'info'
    },
    order_by: 'ends_on',
    get_events_method: 'frappe.desk.doctype.event.event.get_events'
}