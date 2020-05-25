<template>
  <div>
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <a class="navbar-item" href="/">
          <span><b>Watchlists</b></span>
        </a>

        <a
          role="button"
          class="navbar-burger burger"
          aria-label="menu"
          aria-expanded="false"
          data-target="navbarBasicExample"
        >
          <span aria-hidden="true" />
          <span aria-hidden="true" />
          <span aria-hidden="true" />
        </a>
      </div>

      <div id="navbarBasicExample" class="navbar-menu">
        <div class="navbar-start">
          <a class="navbar-item" :href="'/lists/'+loggedInAs">My Lists</a>
          <a class="navbar-item" :href="'/lists'">Explore</a>
          <a class="navbar-item" :href="/create/">Create</a>
        </div>

        <div class="navbar-end">
          <div v-if="loggedInAs">
            <div class="navbar-item">
              <p class="navbar-item">Hello {{loggedInAs}}</p>
              <div class="buttons">
                <b-button type="is-primary" @click="logout" outlined>
                  Log out
                </b-button>
              </div>
            </div>
          </div>
          <div class="navbar-item" v-else>
            <div class="buttons">
              <a class="button is-primary" href="/signUp">
                <strong>Sign up</strong>
              </a>
              <a class="button is-light" href="/login">Log in</a>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <div class="container">
      <nuxt />
    </div>
    <br/>
    <center><p style="color: grey;">© Max S-T 2020</p></center>
  </div>
</template>

<script>
export default {
  data () {
    return {
      loggedInAs: null
    }
  },
  methods: {
    logout () {
      this.$cookies.remove('token')
      location.reload()
    }
  },
  mounted () {
    if (this.$cookies.get('token')) {
      const jwtCookie = this.$cookies.get('token')
      const decodedJwt = JSON.parse(atob(jwtCookie.split('.')[1]))
      const date = new Date()
      const currentTime = date.getTime()
      if (decodedJwt.exp > currentTime) {
        this.logout()
      } else {
        this.loggedInAs = decodedJwt.identity
      }
    }
  }
}
</script>
