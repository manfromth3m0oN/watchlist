<template>
<div>
  <section class="hero is-primary">
    <div class="hero-body">
      <div class="container">
        <h1 class="title">
          List of lists
        </h1>
        <h2 class="subtitle">
          Find something new
        </h2>
      </div>
    </div>
  </section>
  <div class="cont">
    <div v-for="list in lists" v-bind:key="list">
    <Card  :name="list.name" :owner="list.owner" :titles="list.titles" class="card" />
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
      lists: null
    }
  },
  mounted () {
    Axios
      .get('http://localhost:5000/getAll')
      .then(response => (this.lists = JSON.parse(response.data)))
  }
}
</script>

<style scoped>
.card {
  margin: 10px
}
.cont {
  margin-top: 50px;
}
</style>
