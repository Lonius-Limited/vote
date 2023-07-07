<template>
  <div>
    <b-alert show variant="primary"
      ><a href="#" class="alert-link"
        >Here is your list of elections!</a
      ></b-alert
    >
    <b-table
      key="12"
      :fields="fields"
      class="table"
      stacked="md"
      small
      striped
      hover
      :items="electionsForMember"
    >
      <template #cell(action)="row">
        <b-button
          size="sm"
          @click="voteElectionID(row.item.electionID, true)"
          class="mr-1"
          variant="success"
          v-show="row.item.status === 'Open'"
        >
          Vote Now
        </b-button>
        <b-button
          size="sm"
          class="mr-1"
          variant="danger"
          v-show="row.item.status === 'Closed' || row.item.status === 'Open'"
          @click="showResults(row.item.electionID)"
        >
          View Results
        </b-button>
        <b-button
          size="sm"
          class="mr-1"
          variant="info"
          v-show="row.item.status === 'Scheduled'"
          @click="voteElectionID(row.item.electionID, false)"
        >
          View Candidates
        </b-button>
        <b-button
          size="sm"
          class="mr-1"
          variant="warning"
          v-show="row.item.status === 'Scheduled'"
        >
          <b-icon icon="gear-fill" aria-hidden="true"></b-icon>Register
        </b-button>
      </template>
    </b-table>
  </div>
</template>

<script>
export default {
  data () {
    return {
      electionsForMember: [
        { electionID: 1, status: 'Open', scheduledDate: '25/3/2021' },
        { electionID: 2, status: 'Closed', scheduledDate: '22/3/2021' },
        { electionID: 3, status: 'Scheduled', scheduledDate: '25/4/2021' },
        { electionID: 4, status: 'Scheduled', scheduledDate: '28/5/2021' }
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
    voteElectionID: function ($event, $canvote) {
      this.$emit('voteElectionID', {electionID: $event, canVote: $canvote})
    },
    showResults: function ($event) {
      this.$emit('showResults', $event)
    }
  }
}
</script>
