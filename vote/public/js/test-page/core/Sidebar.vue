<template>
  <b-container class="side-bar-area aside-bottom-padding">
    
    <b-row>
      <service-unit-select />
      <b-col cols="12" class="search-input">
        <search-input/>
      </b-col>
      <b-col cols="12" class="no-results" v-if="inSearchMode">
        <b-button v-if="apiList.length === 0" @click="clearSearch">clear </b-button>
      </b-col>
      <b-col cols="12" class="top-margin-space">
        <patient-list
        />
      </b-col>
    </b-row>
  </b-container>
</template>
<script>

export default {
  name: 'SideBar',
  props: {
    selectedBallot: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      placeholder: '      Search ballot...',
      total: 50,
      apiList: [],
      inSearchMode: false,
      searchResultText: 'Searching...',
      currentBallot: null,
      filterdList: [],
    };
  },
  watch: {
    selectedBallot(ballot) {
      if (ballot) {
        this.selectedBallot = ballot;
        this.currentBallot = ballot;
      }
    },
  },
  methods: {},
  components: {

  },
  created() {},
  methods: {
    
  },
};
</script>
<style scoped>
.no-sides {
  margin-left: 0px;
  margin-right: 8px;
}
.side-bar-area {
  background: white;
  width: 100% !important;
  padding-top: 20px;
  min-height: 600px;
  height: 100vh;
  overflow-y: scroll;
}
.name-header {
  background: #687178;
  color: white;
  padding: 14px;
  border-radius: 0px 16px 16px 0px;
  width: 95%;
  font-weight: 800;
}
.search-input {
  margin-top: 5%;
}
.no-results {
  margin-top: 5%;
  padding-left: 7%;
}
.rounded {
  border-radius: 12px;
}
.top-margin-space {
  margin-top: 16px;
  padding-bottom: 16px;
}
.form-control {
  padding: 0.438rem 1rem;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid #d8d6de;
  border-radius: 0.357rem;
  width: 100%;
  height: 2.714rem;
  font-weight: 400;
  line-height: 1.45;
  font-size: 14px;
  color: #6e6b7b;
  -webkit-transition: border-color 0.15s ease-in-out, -webkit-box-shadow 0.15s ease-in-out;
  transition: border-color 0.15s ease-in-out, -webkit-box-shadow 0.15s ease-in-out;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out, -webkit-box-shadow 0.15s ease-in-out;
}

.btn-custom {
  height: 41px;
}
</style>
