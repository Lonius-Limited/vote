<template>
  <div class="container-fluid">
  <div class="row">
    <div class="col-xl-12 col-lg-12 col-md-12">
      <login v-if="showLogin" />
    </div>
  </div>
  </div>
</template>

<script>
import Login from './container/Login.vue'
export default {
  components: {
    Login
  },
  data() {
    return {
      showLogin: true
    };
  },
  computed: {
    
  },
  methods: {
      
  },
};
</script>
