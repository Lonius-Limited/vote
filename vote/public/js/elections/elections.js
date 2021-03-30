import Main from './components/core/Main.vue';

frappe.provide('frappe.elections'); // create a namespace within the Frappe instance
//format date
frappe.elections.ExportTool = class { // create a glue class, wich will manage your Vue instance
    constructor({ parent }) {
        this.$parent = $(parent);
        this.page = parent.page;
        this.setup_header();
        this.make_body();
    }
    make_body() {

        this.$body = this.$parent.find('.layout-main-section');
        this.$parent.find('.page-head').addClass('hidden');
        this.$parent.find('.page-body').removeClass('container');
        this.$parent.find('.content').removeClass('page-container');
        this.$parent.find('.page-content').removeClass('page-content');
        this.$body.removeClass('navbar');
        this.$parent.find('layout-main-section-wrapper').addClass('no-bottom-margin');
        this.$page_container = $('<div class="hub-page-container">').appendTo(this.$body);

        new Vue({
            el: '.hub-page-container',
            render: h => h(Main)
        });
    }

    setup_header() {}
};