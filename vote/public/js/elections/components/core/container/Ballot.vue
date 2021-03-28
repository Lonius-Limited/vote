<template>
    <div class="accordion" role="tablist">
        <b-card no-body class="mb-1" v-for="ballot in ballotDetails" :key="ballot.id">
            <b-card-header header-tag="header" class="p-1" role="tab">
                <b-button block v-b-toggle.accordion-1 variant="info">{{ballot.position}}</b-button>
            </b-card-header>
            <b-collapse id="accordion-1" visible accordion="my-accordion" role="tabpanel">
                <b-card-body>
                    <b-alert show variant="primary" v-if="ballot.enforce_max">You can strictly only vote for <code>{{ballot.max_posts}}</code> candidates below.</b-alert>
                    <b-alert show variant="primary" v-if="!ballot.enforce_max">You may vote for up to a maximum of <code>{{ballot.max_posts}}</code> candidates below.</b-alert>
                    
                    <b-table key="12"  :fields="fields" class="table" stacked="md" small striped hover :items="ballot.candidates">
                        <template #cell(action)="row">   
                            <div>
                                <b-row>
                                    <b-col>
                                        
                                    </b-col>
                                </b-row>
                            </div>
                        </template>
                    </b-table>
                </b-card-body>
            </b-collapse>
        </b-card>
    </div>
</template>

<script>
    export default {
        data(){
            return{
                ballotDetails: [
                    {
                        "id": "1",
                        "position": "President",
                        "max_posts": 1,
                        "enforce_max": true,
                        "candidates": [
                            {
                                "id": 1,
                                "name": "Uhuru Kenyatta",
                                "party": "Jubilee",
                                "symbol": "Jogoo",
                                "image": "",
                                "voted": false
                            },
                            {
                                "id": 2,
                                "name": "Raila Odinga",
                                "party": "ODM",
                                "symbol": "Orange",
                                "image": "",
                                "voted": false
                            },
                            {
                                "id": 3,
                                "name": "Mwalimu Dida",
                                "party": "Whatever",
                                "symbol": "Something",
                                "image": "",
                                "voted": false
                            }
                        ]
                    },
                    {
                        "id": "2",
                        "position": "Senator",
                        "max_posts": 2,
                        "enforce_max": false,
                        "candidates": [
                            {
                                "id": 1,
                                "name": "Samson Cherargei",
                                "party": "Jubilee",
                                "symbol": "Jogoo",
                                "image": "",
                                "my_choice": false
                            },
                            {
                                "id": 2,
                                "name": "James Orengo",
                                "party": "ODM",
                                "symbol": "Orange",
                                "image": "",
                                "my_choice": false
                            },
                            {
                                "id": 3,
                                "name": "Someone Wamatangi",
                                "party": "Whatever",
                                "symbol": "Something",
                                "image": "",
                                "my_choice": false
                            }
                        ]
                    }
                ],
                fields: [
                    'id',
                    'image',
                    'name',
                    'party',
                    'symbol',
                    'my_choice',
                    { label: 'Actions', key: 'action' }
                ]
            }
        },
        props: ['thisElectionId'],
        methods: {

        },
        created(){
            alert("The prop passed in here is: " + this.thisElectionId + ". Now we can retrieve the election details.")
        }
    }
</script>

