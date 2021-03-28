<template>
    <div>
        <b-alert show variant="primary"><a href="#" class="alert-link">Here is your list of elections!</a></b-alert>
        <b-table key="12"  :fields="fields" class="table" stacked="md" small striped hover :items="electionsForMember">
            <template #cell(action)="row">
                <div>
                    <b-row>
                        <b-col lg="3" class="pb-2" v-show="row.item.status === 'Open'">
                            <b-button block
                            class="btn btn-success btn-sm" variant="success"
                            @click="voteElectionID(row.item.electionID)"
                            >Vote Now</b-button>
                        </b-col>
                        <b-col lg="3" class="pb-2" v-show="row.item.status === 'Closed' || row.item.status === 'Open'">
                            <b-button block 
                            class="btn btn-danger btn-sm"
                            >View Results</b-button>
                        </b-col>
                        <b-col lg="3" class="pb-2" v-show="row.item.status === 'Scheduled'">
                            <b-button block 
                            class="btn btn-primary btn-sm"
                            >View Candidates</b-button>
                        </b-col>
                    </b-row>
                </div>
            </template>
        </b-table>
    </div>
</template>

<script>
    export default {
        data(){
            return{
                electionsForMember: [
                    {electionID: 1, status: "Open", scheduledDate: "25/3/2021"},
                    {electionID: 2, status: "Closed", scheduledDate: "22/3/2021"},
                    {electionID: 3, status: "Scheduled", scheduledDate: "25/4/2021"},
                    {electionID: 4, status: "Scheduled", scheduledDate: "28/5/2021"}
                ],
                fields: [
                    'electionID',
                    'status',
                    'scheduledDate',
                    { label: 'Actions', key: 'action' }
                ]
            }
        },
        methods: {
            voteElectionID: function($event){
                this.$emit('voteElectionID', $event)
            }
        }
    }
</script>

