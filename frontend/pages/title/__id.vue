<template>
<div>
  <div v-if="showData">
  <section class="hero is-primary">
    <div class="hero-body">
      <div class="container">
        <h1 class="title">
          {{ title }}
        </h1>
        <h2 class="subtitle">
          {{ showData.Writer }}
        </h2>
      </div>
    </div>
  </section> <br/>
  <div class="columns">
    <div class="column is-9">
      <p class="subtitle is-5">
        Cast: {{showData.Actors}} <br/><br/>
        Plot:
      </p>
      <p class="plot">{{showData.Plot}}</p> <br/>
      <p>Type: {{showData.Type}}, Runtime: {{showData.Runtime }}, Language: {{showData.Language}}, IMDB Rating: {{showData.imdbRating}}, <a :href="'https://www.imdb.com/title/'+showData.imdbID">IMDB</a></p>
    </div>
    <div class="column is-3" v-if="showData">
      <img :src="showData.Poster" />
    </div>
  </div>
  </div>
  <div v-else>
    Nothing here
  </div>
</div>
</template>

<script>
import Axios from 'axios'

export default {
  data () {
    return {
      title: this.$route.path.split('/').slice(-1)[0],
      showData: null
    }
  },
  mounted () {
    Axios
      .get('http://www.omdbapi.com/?apikey=cfe0ffdb&plot=full&t=' + this.title)
      .then(response => (this.showData = response.data))
  }
}
</script>

<style scoped>
.plot {
  margin-top: -20px
}
</style>
