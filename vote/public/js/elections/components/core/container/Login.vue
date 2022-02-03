<template>
    <div>
        <b-jumbotron header="Vote Online" lead="Welcome to transparency! Vote efficiently, effectively and safely">
            <p>Please login by pressing the button below using your Institution's Member ID together with the Voter ID that you received in your email/SMS. We will send you an OTP for verification. This ensures you vote securely!</p>
            <b-button block variant="primary" href="#" @click="modalShow = !modalShow">Login</b-button>
        </b-jumbotron>
        <div>
            

            <b-modal ref="login-modal"  v-model="modalShow">
               <b-input-group prepend="Voter ID: " class="mt-3">
                <b-form-input id="voter-id" v-model="voterID"></b-form-input>
              </b-input-group>
              <b-input-group prepend="Member ID: " class="mt-3">
                <b-form-input id="member-id" v-model="memberID"></b-form-input>
              </b-input-group>
              <b-input-group prepend="OTP Code: " v-show="timeToEnterOtp" class="mt-3">
                <b-form-input id="otp-code" v-model="otpCode"></b-form-input>
              </b-input-group>
              <button @click="Login">Login</button>
            </b-modal> 
        </div>
    </div>
</template>

<script>
  export default {
    data() {
      return {
        modalShow: false,
        timeToEnterOtp: false
      }
    },
    methods: {
      formatterUpperCase(value) {
        return value.toUpperCase()
      }, 
      Login: function(){
        if(!this.timeToEnterOtp){
          //post_memberID_and_voterID() and send OTP to user. Show OTP box
          this.timeToEnterOtp = true
        }else{
          //VERYFY OTP. ON RETURN IF WE ARE SUCCESSFUL, CLOSE MODAL AND TURN OFF HOME PAGE. LOAD ELECTIONS
          this.$refs['login-modal'].hide()
          this.$emit("login-succeeded", this.memberID)
        }
      }
    }
  }
</script>