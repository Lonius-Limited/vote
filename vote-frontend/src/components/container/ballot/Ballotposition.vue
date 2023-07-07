<template>
    <b-collapse id="ballot" visible accordion="my-accordion" role="tabpanel">
        <b-card-body>
            <b-table key="12" selectable ref="ballotTable" :select-mode="selectMode" selected-variant="info" @row-selected="onRowSelected" @row-clicked = "lastSelection" :fields="ballotFields" class="table" stacked="md" small striped hover :items="ballotData" responsive="sm">
                <template #cell(voted_for)="{ rowSelected }">
                    <template v-if="rowSelected">
                        <span aria-hidden="true">&check;</span>
                        <span class="sr-only">Selected</span>
                    </template>
                    <template v-else>
                        <span aria-hidden="true">&nbsp;</span>
                        <span class="sr-only">Not selected</span>
                    </template>
                </template>
            </b-table>
            <!-- <p>{{selected}}</p> -->
        </b-card-body>
    </b-collapse>
</template>

<script>
export default {
  data () {
    return {
      selectMode: 'multi',
      selected: [],
      lastSelected: null
    }
  },
  props: ['ballotData', 'ballotFields', 'maxForPosition', 'votingEnabled'],
  methods: {
    onRowSelected (items) {
      if (this.votingEnabled) {
        this.selected = items
        if ((items.length) > this.maxForPosition) {
          this.$bvToast.toast(`You have exceeded the maximum number of candidates you can vote for (${this.maxForPosition}). To remove selected candidate, click on them again.`, {
            title: 'Maximum Number of Votes Reached',
            autoHideDelay: 5000,
            variant: 'danger',
            solid: true,
            toaster: 'b-toaster-bottom-right'
          })
          this.$refs.ballotTable.unselectRow(this.lastSelected)
        }
      } else {
        this.$refs.ballotTable.unselectRow(this.lastSelected)
      }
    },
    lastSelection (item, index) {
      // alert("Last selected: " + index);
      this.lastSelected = index
    }
  }
}
</script>
