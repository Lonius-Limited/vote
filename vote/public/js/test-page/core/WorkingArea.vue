<template>
  <b-container class="area-background">
    <b-row>
    <b-col class="patient-info">
        <b-card style="width: 100%;" no-body class="top-menu cardx" v-if="selectedBallot"
          ></b-card>
      </b-col>
      <b-col cols="12" class="" v-if="selectedBallot">
        <b-card no-body class="top-menu cardx"
          ><patient-chart
            
          />
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>
<script>

export default {
  name: 'WorkingArea',
  data() {
    return {
      lastAction: '',
      currentTabActions: [],
      currentTabButtons: [],
    };
  },
  props: {
    selectedBallot: Object
  },
  watch: {
    selectedBallot() {
      
    },
  },
  methods: {
    
  },
  created() {
    
  },
  mounted() {
    
  },
  components: {
    
  },
};
</script>
<style scoped>
.top-menu {
  padding: 0px !important;
}
.section-margin-space {
  margin-top: 3%;
}
.cardx {
  box-shadow: 0 0px 0px 0 rgb(0 0 0 / 20%) !important;
  transition: 0.3s;
  border-radius: 7px !important;
}
.area-background {
  padding-left: 0px !important;
  padding-right: 0px !important;
}
.highest-card {
  z-index: 1;
}

</style>
