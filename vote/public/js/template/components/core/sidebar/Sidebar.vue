<template>
  <div>
    <ul
      class="nav nav-pills nav-stacked"
      v-for="appointment in appointments"
      :key="appointment.name"
    >
      <li role="presentation">
        <SidebarItem
          class="sidebar-item"
          :appointment="appointment"
          @appointmentClicked="appointmentClicked"
        />
      </li>
    </ul>
  </div>
</template>
<script>
import SidebarItem from "./SidebarItem.vue";
export default {
  components: {
    SidebarItem,
  },
  data() {
    return {
      appointments: [],
    };
  },
  methods: {
    appointmentClicked(appointment) {
      this.$emit("appointmentClicked", appointment);
    },
  },
  created() {
    frappe.call({
      method:
        "clinical.api.nurses_portal.get_appointments",
      args: {
        start: 0,
        page_length: 20,
      },
      callback: function (r) {
        var data = r.message;
        //console.log(data);
        if (data.length) {
          this.appointments = data;
        }
      },
    });
  },
  mounted() {
    frappe.call({
      method:
        "clinical.api.nurses_portal.get_appointments",
      args: {
        start: 0,
        page_length: 20,
      },
      callback: (r) => {
        var data = r.message;
        console.log(data);
        if (data.length) {
          this.appointments = data;
        }
      },
    });
  },
};
</script>
<style lang="sass"></style>
