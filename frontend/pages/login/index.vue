<template>
  <section>
    <div class="login">
    <h1 class="title">Login</h1>
      <b-field
        label="Username"
      >
          <b-input v-model="username"></b-input>
      </b-field>

      <b-field
          label="Password"
          >
          <b-input
            type="password"
            v-model="password"
            ></b-input>
      </b-field>
      <div class="columns">
        <div class="column is-11"></div>
        <div class="column is-1">
          <b-button type="is-primary" @click="login">Submit</b-button>
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
      username: null,
      password: null,
      passHash: null
    }
  },
  methods: {
    checkCookie (response) {
      if (Object.keys(response)[0] === 'msg') {
        console.log('Incorrect Login')
      } else {
        this.$cookies.set('token', response.access_token)
        window.location.href = '/'
      }
    },
    login () {
      this.passHash = SHA256(this.password).toString()
      Axios
        .post('http://localhost:5000/login', { 'username': this.username, 'passwordHash': this.passHash })
        // .then(response => (console.log(Object.keys(response.data))))
        .then(response => (this.checkCookie(response.data)))
        .catch(error => (console.log(error)))
    }
  }
}
</script>

<style scoped>
.login {
  margin:50px
}
</style>
