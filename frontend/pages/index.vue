<template>
<div>
  <section class="hero is-medium is-primary is-bold has-text-centered">
    <div class="hero-body">
      <div class="container">
        <h1 class="title">Watchlists</h1>
        <h2 class="subtitle">A simple way to track your watchlists</h2>
      </div>
    </div>
  </section>
  <hr />
  <section>
    <div class="popular">
      <h1 class="title has-text-centered">Some random lists to get started</h1>
      <div v-for="list in lists" v-bind:key="list.name">
        <Card :name="list.name" :owner="list.owner" :titles="list.titles" class="card" />
      </div>
    </div>
  </section>
</div>
</template>

<script>
import axios from 'axios'
import Card from '../components/Card.vue'

export default {
  name: 'Index',
  components: {
    Card
  },
  data () {
    return {
      lists: null
    }
  },
  mounted () {
    axios
      .get('http://localhost:5000/head')
      .then(response => (this.lists = response.data))
  }
}
</script>

<style scoped>
.popular {
  margin-top: 20px;
}
.card {
  margin: 10px;
}
</style>
