<template>
    <div>
        <b-card no-body class="mb-1" v-for="result in results" :key="result.id">
            <b-card-header header-tag="header" class="p-1" role="tab">
                <b-button block variant="success" > <h3>Position: {{ result.position }}</h3></b-button>
            </b-card-header>
            <result :results="result" />
        </b-card>
    </div>
</template>
<script>
import Result from "./result/Result.vue"

export default {
    components: { Result },
    data(){
        return {
            results: [
                {
                    id: 1,
                    position: "President",
                    ballots: 5000,
                    tally: [
                        {id: 1, candidate: "Uhuru Kenyatta", votes: 2300},
                        {id: 2, candidate: "Raila Odinga", votes: 1500},
                        {id: 3, candidate: "Dida Someonelse", votes: 170}
                    ]
                },
                {
                    id: 2,
                    position: "Senator",
                    ballots: 5000,
                    tally: [
                        {id: 4, candidate: "Samson Cherargei", votes: 1400},
                        {id: 5, candidate: "Kipchumba Murkomen", votes: 1200},
                        {id: 6, candidate: "Wamatangi Someoneelse", votes: 1100}
                    ]
                }
            ]
        }
    },
    props: ["electionID"],
    methods: {

    },
    created(){
        //GET THE RESULTS BASED ON THIS.ELECTIONID

    }
}
</script>