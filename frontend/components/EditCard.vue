<template>
<div>
  <div v-if="showData">
    <div class="box columns padding">
      <div class="column is-2">
        <img :src="showData.Poster" />
      </div>
      <div class="column is-8">
        <h4 class="title is-4">
          {{title}}
        </h4>
        <h6 class="subtitle is-6">
          Directed by: {{ showData.Director }}, Writen by: {{ showData.Writer}}
        </h6>
        <strong>Cast:</strong> {{ showData.Actors }} <br/>
        <strong>Plot: </strong>{{ showData.Plot }} <br/>
        <div v-if="showData.Ratings">
          <strong>Ratings: </strong>{{showData.Ratings[0].Source}} - {{showData.Ratings[0].Value}}
        </div>
      </div>
      <div class="field column is-1">
        <b-switch v-model="watched.watched" @input="updateWatched">
          {{ watchedTF[watched.watched] }}
        </b-switch>
        <b-button @click="this.delete" type="is-danger">Delete</b-button>
      </div>
    </div>
  </div>
  <div v-else>

  </div>
</div>
</template>

<script>
import Axios from 'axios'
export default {
  props: ['title', 'list', 'watched'],
  data () {
    return {
      showData: null,
      watchedTF: { true: 'Watched', false: 'Unwatched' }
    }
  },
  mounted () {
    Axios
      .get('http://www.omdbapi.com/?apikey=cfe0ffdb&t='.concat(this.title))
      .then(response => (this.showData = response.data))
  },
  methods: {
    updateWatched () {
      Axios
        .post('http://localhost:5000/updateWatchedStatus', { 'name': this.list, 'showTitle': this.title, 'watchedStatus': this.watched.watched }, { headers: { Authorization: `Bearer ${this.$cookies.get('token')}` } })
        .then(response => (console.log(response)))
    },
    delete () {
      Axios
        .post('http://localhost:5000/removeTitle', { 'title': this.title, 'list': this.list }, { headers: { Authorization: `Bearer ${this.$cookies.get('token')}` } })
        .then(function (response) {
          console.log(response)
          location.reload()
        }
        )
    }
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
</style>
