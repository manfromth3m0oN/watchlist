<template>
<div v-if="showInfo" v-on:input="$emit('watched', title, watched)">
  <div v-if="showInfo.Title">
  <div class="box columns padding">
    <div class="column is-2">
      <div v-if="showInfo.Poster">
        <img :src="showInfo.Poster" />
      </div>
    </div>
    <div class="column is-8">
      <h4 class="title is-4">
        {{ title }}
      </h4>
      <h6 class="subtitle is-6">
        Directed by: {{ showInfo.Director }}, Writen by: {{ showInfo.Writer}}
      </h6>
      <strong>Cast:</strong> {{ showInfo.Actors }} <br/>
      <strong>Plot: </strong>{{ showInfo.Plot }} <br/>
      <div v-if="showInfo.Ratings">
      <strong>Ratings:</strong> {{ showInfo.Ratings[0].Source }} - {{ showInfo.Ratings[0].Value }}
      </div>
    </div>
  </div>
</div>
<article class="message is-danger" v-else>
  <div class="message-header">
    <p>No Database entry for {{ title }}</p>
  </div>
  <div class="message-body">
    The title {{ title }} could not be fetched from the Open Movie Database. If you think this is an error report it <a src="https://www.omdbapi.com/">here</a> Find out more at <a href="https://www.omdbapi.com/">https://www.omdbapi.com/</a>
  </div>
</article>
</div>
</template>

<script>
import Axios from 'axios'
export default {
  props: {
    title: {
      type: String,
      required: true
    },
    watched: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      showInfo: null
    }
  },
  mounted () {
    Axios
      .get('http://www.omdbapi.com/?apikey=cfe0ffdb&t='.concat(this.title))
      .then(response => (this.showInfo = response.data))
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
.center {
  margin: 50%;
  position: absolute;
}
</style>
