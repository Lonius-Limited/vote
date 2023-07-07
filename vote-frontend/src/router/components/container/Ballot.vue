<template>
    <div class="accordion" role="tablist">
        <b-card no-body class="mb-1" v-for="ballot in ballotDetails" :key="ballot.id">
            <b-card-header header-tag="header" class="p-1" role="tab">
                <b-button block variant="success" v-if="ballot.enforce_max">Position: {{ballot.position}} - You can strictly only vote for {{ballot.max_posts}} candidates below.</b-button>
                <b-button block variant="success" v-if="!ballot.enforce_max">Position: {{ballot.position}} - You may vote for up to a maximum of {{ballot.max_posts}} candidates below.</b-button>
            </b-card-header>
            <ballotposition :key="ballot.id" :ballotData="ballot.candidates" :votingEnabled="votingEnabled" :ballotFields="fields" :maxForPosition="ballot.max_posts" />

        </b-card>
    </div>
</template>

<script>
import Ballotposition from './ballot/Ballotposition.vue'
export default {
  components: { Ballotposition },
  data () {
    return {
      ballotDetails: [
        {
          'id': '1',
          'position': 'President',
          'max_posts': 1,
          'enforce_max': true,
          'candidates': [
            {
              'id': 1,
              'name': 'Uhuru Kenyatta',
              'party': 'Jubilee',
              'symbol': 'Jogoo',
              'image': '',
              'voted': false
            },
            {
              'id': 2,
              'name': 'Raila Odinga',
              'party': 'ODM',
              'symbol': 'Orange',
              'image': '',
              'voted': false
            },
            {
              'id': 3,
              'name': 'Mwalimu Dida',
              'party': 'Whatever',
              'symbol': 'Something',
              'image': '',
              'voted': false
            }
          ]
        },
        {
          'id': '2',
          'position': 'Senator',
          'max_posts': 2,
          'enforce_max': false,
          'candidates': [
            {
              'id': 4,
              'name': 'Samson Cherargei',
              'party': 'Jubilee',
              'symbol': 'Jogoo',
              'image': '',
              'my_choice': false
            },
            {
              'id': 5,
              'name': 'James Orengo',
              'party': 'ODM',
              'symbol': 'Orange',
              'image': '',
              'my_choice': false
            },
            {
              'id': 6,
              'name': 'Someone Wamatangi',
              'party': 'Whatever',
              'symbol': 'Something',
              'image': '',
              'my_choice': false
            }
          ]
        }
      ],
      fields: [
        'voted_for',
        'id',
        'image',
        'name',
        'party',
        'symbol'
      ]
    }
  },
  props: ['thisElectionId', 'votingEnabled'],
  methods: {

  },
  created () {
    // alert("The prop passed in here is: " + this.votingEnabled + ". Now we can retrieve the election details.")
  }
}
</script>
