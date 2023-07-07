<template>
  <div class="container-fluid">
  <div class="row">
    <div class="col-xl-12 col-lg-12 col-md-12">
      <login
        v-if="showLogin"
        @login-succeeded="LoginSuccess"
        :base_url = base_url
      />
      <list-elections
        v-if="!showLogin && !showBallot && !resultsVisible"
        v-on:voteElectionID="voteElectionID($event, $canvote)"
        v-on:showResults = "showResults($event)"
      />
      <ballot
        v-if="!showLogin && showBallot && !resultsVisible"
        :this-election-id = "activeBallotID"
        :voting-enabled = "votingEnabled"
      />
      <Results
        v-if="!showLogin && !showBallot && resultsVisible"
        :electionID="activeBallotID"
      />

    </div>
  </div>
  </div>
</template>

<script>
import Ballot from './components/container/Ballot.vue'
import ListElections from './components/container/ListElections.vue'
import Login from './components/container/Login.vue'
import Results from './components/container/Results.vue'
export default {
  components: {
    Login,
    ListElections,
    Results,
    Ballot
  },
  data () {
    return {
      showLogin: true,
      showBallot: false,
      activeBallotID: 0,
      votingEnabled: false,
      resultsVisible: false,
      base_url: 'https://vote.bizpok.com/api/method'
    }
  },
  computed: {

  },
  methods: {
    LoginSuccess: function ($event) {
      this.showLogin = false
    },
    voteElectionID: function ($event) {
      // GET THE ELECTION DETAILS BASED ON EVENT
      this.activeBallotID = $event.electionID
      this.votingEnabled = $event.canVote
      this.showBallot = true
    },
    showResults: function ($event) {
      // GET THE ELECTION RESULTS BASED ON ELECTION ID PASSED IN EVENT ARGUMENT
      this.resultsVisible = true
      this.activeBallotID = $event
    }
  }
}
</script>
