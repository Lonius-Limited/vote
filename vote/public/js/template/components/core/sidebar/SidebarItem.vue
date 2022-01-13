<template>
  <div>
   <span class="sidebar-item-label" @click="renderDetails()">
     {{ appointment.patient_name }}-{{ appointment.name }}
     <span>
				</span></span>
  </div>
  
</template>
<script>
export default {
  props: {
    appointment: {
      type: Object,
      default: {},
      required: true,
    },
  },
  methods: {
    renderDetails() {
      this.$emit("appointmentClicked", this.appointment);
    },
  },
};
</script>
