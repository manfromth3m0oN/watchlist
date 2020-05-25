<template>
  <div>
    <section class="hero is-primary">
  <div class="hero-body">
    <div class="container">
      <h1 class="title">
        {{user}}'s Lists
      </h1>
    </div>
  </div>
</section>
  <div v-if="lists">
    <div v-for="list in lists" :key="list">
      <Card :title="list.name" :owner="list.owner" :titles="list.titles" />
    </div>
  </div>
  </div>
</template>

<script>
import Axios from 'axios'
import Card from '../../components/Card'

export default {
  components: {
    Card
  },
  data () {
    return {
      user: null,
      lists: null
    }
  },
  mounted () {
    if (this.$cookies.get('token')) {
      const jwtCookie = this.$cookies.get('token')
      const decodedJwt = JSON.parse(atob(jwtCookie.split('.')[1]))
      this.user = decodedJwt.identity
    }
    Axios
      .get('http://localhost:5000/getAll/'.concat(this.user))
      .then(response => (this.lists = response))
  }
}
</script>

<style>

</style>
