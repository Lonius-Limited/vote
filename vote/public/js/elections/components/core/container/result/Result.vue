<template>
    <div>
        <div>
            <h3>
            <span class="col-sm-3">Eligible Voters: <b-badge variant="primary"> {{ totalBallots }} </b-badge></span>
            <span class="col-sm-3">Total Voted: <b-badge variant="success"> {{ totalVoted }} </b-badge></span>
            <span class="col-sm-3">Yet to Vote: <b-badge variant="warning"> {{ yetToVote }} </b-badge></span>
            <span class="col-sm-3">Percentage Turnout: <b-badge variant="danger"> {{ turnOut }}% </b-badge></span>
            </h3>
        </div>
        <div :key="candidate.id" v-for="candidate in results.tally" class="row mb-3">
            
        <div class="col-sm-3"><b-avatar class="mr-3"></b-avatar>{{ candidate.candidate }}:</div>
        <div class="col-sm-9 pt-1">
            <b-progress :max="maxForHighestCandidate" height="20px" variant="danger" :key="candidate.id">
                <b-progress-bar :value="candidate.votes" >
                    <span><strong>{{ candidate.votes }}</strong></span>
                </b-progress-bar>
            </b-progress>
        </div>
        </div>
  </div>
</template>
<script>
export default {
    data(){
        return{
            yetToVote: 0,
            maxForHighestCandidate: 0,
            totalVoted: 0,
            totalBallots: 0,
            turnOut:0
        }
    },
    props: ["results"],
    created(){
        //CALCULATE THE MAXIMUM THAT THE HIGHEST CANDIDATE CAN GET.
        console.log("results: " + JSON.stringify(this.results));
        //var totalVoted = this.results.map(result => result.tally.votes).reduce((thisvote, totalvotes) => totalvotes + thisvote);
        var totalWhoHaveVoted = this.results.tally.map(result => result.votes).reduce((thisvote, totalvotes) => totalvotes + thisvote);
        var totalExpectedToVote = this.results.ballots;
        this.totalBallots = this.numberWithCommas(totalExpectedToVote);
        //var highestVotesForACandidate = this.results.map(result => result.tally.votes).reduce((currentBigVote, candidate) => currentBigVote = currentBigVote > candidate.votes ? currentBigVote : candidate.votes, 0);
        var highestVotesForACandidate = this.results.tally.map(result => result.votes).reduce((currentBigVote, thisVote) => currentBigVote = currentBigVote > thisVote ? currentBigVote : thisVote, 0);
        var toVote = totalExpectedToVote - totalWhoHaveVoted;
        this.yetToVote = this.numberWithCommas(toVote);
        this.totalVoted = this.numberWithCommas(totalWhoHaveVoted);
        this.maxForHighestCandidate = highestVotesForACandidate + toVote;
        this.turnOut = ((totalWhoHaveVoted/totalExpectedToVote) * 100).toFixed(1);
        //alert("totalVoted: " + totalVoted + ", highestVotesForACandidate: " + highestVotesForACandidate + ", yetToVote: " + this.yetToVote + ", maxForHighestCandidate: " + this.maxForHighestCandidate)
    },
    methods: {
        numberWithCommas: function(aNumber){
            return aNumber.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
    }
}
</script>