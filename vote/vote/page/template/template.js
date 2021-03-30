frappe.pages['template'].on_page_load = function(wrapper) {
    this.page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'None',
        single_column: true
    });

    this.page.$export_tool = new frappe.vote.ExportTool(this.page)
}