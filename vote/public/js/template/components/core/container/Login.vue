<template>
    <div>
        <b-jumbotron header="Vote Online" lead="Welcome to the new way of doing things. Vote efficiently, transparently and safely">
            <p>Please login below. You will have received your Institution Member ID in your email. We will send you an OTP for verification. This ensures you vote securely!</p>
            <b-button block variant="primary" href="#" @click="modalShow = !modalShow">Login</b-button>
        </b-jumbotron>
        <div>
            

            <b-modal v-model="modalShow">You will login from here!</b-modal>
        </div>
    </div>
</template>

<script>
  export default {
    data() {
      return {
        modalShow: false
      }
    }
  }
</script>