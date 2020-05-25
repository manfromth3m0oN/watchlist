<template>
<section>
  <div class="signup">
    <h1 class="title">Signup</h1>
    <b-field
      label="Username"
    >
      <b-input v-model="username"></b-input>
    </b-field>
    <b-field
      label="Email"
    >
      <b-input v-model="email"></b-input>
    </b-field>
    <b-field
      label="Password"
      >
        <b-input
          type="password"
          v-model="password"
          ></b-input>
    </b-field>
    <div>
      <br/>
      <div class="columns">
        <div class="column is-11"></div>
        <div class="colum is-1">
          <b-button type="is-primary" @click="register">Submit</b-button>
        </div>
      </div>
    </div>
  </div>
</section>
</template>

<script>
import Axios from 'axios'
const SHA256 = require('crypto-js/sha256')

export default {
  data () {
    return {
      email: null,
      username: null,
      password: null,
      passHash: null
    }
  },
  methods: {
    register () {
      this.passHash = SHA256(this.password).toString()
      Axios
        .post('http://localhost:5000/register', { 'email': this.email, 'username': this.username, 'passwordHash': this.passHash })
        .then(response => (console.log(response)))
    }
  }
}
</script>

<style scoped>
.signup {
  margin: 50px;
}
</style>
