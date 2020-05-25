<template>
  <div class="box columns view">
    <div class="column is-2" v-if="poster">
      <img :src="poster" />
    </div>
    <div class="column is-8">
      <h4 class="title is-4">
        {{ name }}
      </h4>
      <h6 class="subtitle is6">
        Made by: {{ owner }}
      </h6>
      <ul>
        <li v-for="(status, title) in titles" :key="title">{{ title }}</li>
      </ul>
    </div>
    <div class="column is-2">
      <a class="button is-primary is-light" :href="name">
        See more
      </a>
    </div>
  </div>
</template>

<script>
import Axios from 'axios'
export default {
  props: {
    name: {
      type: String,
      required: true
    },
    owner: {
      type: String,
      required: true
    },
    titles: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      poster: null,
      titlesList: this.titles
    }
  },
  mounted () {
    Axios
      .get('http://www.omdbapi.com/?apikey=cfe0ffdb&t='.concat(Object.keys(this.titlesList)[0]))
      .then(response => (this.poster = response.data.Poster))
  }
}
</script>

<style scoped>
ul {
    height: 50px;
    -moz-columns: 3 200px;
    -webkit-columns: 3 200px;
    columns: 3 200px;
}
.view {
  overflow: hidden;
}
</style>
