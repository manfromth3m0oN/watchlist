<template>
  <div>
    <div v-if="listDetail">
          <section class="hero is-primary">
      <div class="hero-body">
        <div class="container">
          <div class="columns">
            <div class="column is-10">
              <h1 class="title">
                Edit: {{ listDetail.name }}
              </h1>
              <h3 class="subtitle" v-if="listDetail">
                Created by: {{ listDetail.owner }}
              </h3>
            </div>
          </div>
        </div>
      </div>
    </section>
    <center class="padded">
      <b-field label="Add title">
        <b-input placeholder="A title" v-model="titleToAdd"></b-input>
      </b-field>
      <b-button type="is-primary" @click="findTitle">Submit</b-button>
     </center>
     <div v-if="showDataToAdd">
       <div class="box columns padding">
         <div class="column is-2">
           <img :src="showDataToAdd.Poster" />
         </div>
         <div class="column is-8">
           <h4 class="title is-4">
             {{ showDataToAdd.Title }}
           </h4>
           <h6 class="subtitle is-6">
             Directed by: {{ showDataToAdd.Director }}, Writen by: {{ showDataToAdd.Writer}}
           </h6>
           <strong>Cast:</strong> {{ showDataToAdd.Actors }} <br/>
          <strong>Plot: </strong>{{ showDataToAdd.Plot }} <br/>
          <div v-if="showDataToAdd.Ratings">
            <strong>Ratings:</strong> {{ showDataToAdd.Ratings[0].Source }} - {{ showDataToAdd.Ratings[0].Value }}
          </div>
         </div>
         <div class="field column is-2">
           <center>
           Is this right? <br/>
           <a class="button is-success" @click="addShow">Yes</a>
           <a class="button is-danger" @click="showIncorrect">No</a>
           </center>
         </div>
       </div>
     </div>
     <div v-for="(watched, title) in listDetail.titles" :key="title" class="columns title-cards">
       <AddCard :title="title" :watched="listDetail.titles[title]" />
     </div>
    </div>
    <div v-else>
      No list named {{ this.$route.path.replace(/\/add\//g, '') }}
    </div>
  </div>
</template>

<script>
import Axios from 'axios'
import AddCard from '../../components/AddCard'

export default {
  components: {
    AddCard
  },
  data () {
    return {
      listDetail: null,
      titleToAdd: null,
      showDataToAdd: null
    }
  },
  beforeMount () {
    const path = this.$route.path
    Axios
      .get('http://localhost:5000/get/'.concat(encodeURI(path.replace(/\/add\//g, ''))))
      .then(response => (this.listDetail = JSON.parse(response.data)))
  },
  methods: {
    findTitle () {
      Axios
        .get('http://www.omdbapi.com/?apikey=cfe0ffdb&t='.concat(this.titleToAdd))
        .then(response => (this.showDataToAdd = response.data))
    },
    showIncorrect () {
      this.showDataToAdd = null
    },
    addShow () {
      Axios
        .post('http://localhost:5000/addToList', { 'name': this.listDetail.name, 'titles': [this.showDataToAdd.Title] }, { headers: { Authorization: `Bearer ${this.$cookies.get('token')}` } })
        .then(function (response) {
          console.log(response)
          this.$buefy.modal.open(
            `<p>
                Added successfully
            </p>`
          )
          location.reload()
        })
    }
  }
}
</script>

<style scoped>
.padded {
  padding-top: 10px;
  padding-bottom: 10px;
}
.title-cards {
  padding-top: 30px;
}
</style>
