<template>
  <div class="container-fluid">
  <div class="row">
    <div class="col-xl-12 col-lg-12 col-md-12">
      <login 
        v-if="showLogin" 
        @login-succeeded="LoginSuccess" 
      />
      <list-elections 
        v-if="!showLogin && !showBallot" 
        v-on:voteElectionID="voteElectionID($event)" 
      />
      <ballot 
        v-if="showBallot"
        :this-election-id = "activeBallotID"
      />
    </div>
  </div>
  </div>
</template>

<script>
import Ballot from './container/Ballot.vue';
import ListElections from './container/ListElections.vue';
import Login from './container/Login.vue';
export default {
  components: {
    Login,
    ListElections,
    Ballot
  },
  data() {
    return {
      showLogin: false,
      showBallot: false,
      activeBallotID: 0
    };
  },
  computed: {
    
  },
  methods: {
      LoginSuccess: function($event){
        this.showLogin = false
      },
      voteElectionID: function($event){
        //GET THE ELECTION DETAILS BASED ON EVENT
        this.activeBallotID = $event;
        this.showBallot = true;
      }
  },
};
</script>
