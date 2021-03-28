frappe.pages['elections'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Elections',
        single_column: true
    });

    page.$export_tool = new frappe.elections.ExportTool(page)
}