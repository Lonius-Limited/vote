frappe.pages['election-results'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Election Results',
		single_column: true
	});
}