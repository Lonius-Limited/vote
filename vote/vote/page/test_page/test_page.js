frappe.pages['test-page'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Test Page',
        single_column: true
    });

    page.$export_tool = new frappe.testpage.TestChart(page)
        //page.$export_tool = new frappe.nursing.ExportTool(page);
    console.log("testpage: " + page);
}