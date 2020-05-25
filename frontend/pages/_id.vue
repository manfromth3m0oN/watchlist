/* eslint-disable */
<template>
  <div>
    <div v-if="listDetail">
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container">
          <div class="columns">
            <div class="column is-10">
              <h1 class="title">
                {{ listId }}
              </h1>
              <h3 class="subtitle">
                Created by: {{ listDetail.owner }}
              </h3>
            </div>
            <div>
              <div class="column is-2" v-if="loggedInAs === listDetail.owner">
                <a :href="'/edit/'+listId" class="button">Edit Watched Status</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <div class="title-container">
      <div v-for="(watched, title) in listDetail.titles" :key="title" class="columns title-cards">
          <ShowCard :title="title" :watched="listDetail.titles[title]" />
      </div>
      <a class="box" :href="'/add/'+listId">
        <h1 class="title big">+</h1>
        <h4 class="subtitle add">Add title</h4>
      </a>
    </div>
    </div>
    <div v-else>
      <b-loading :active.sync="loading"></b-loading>
    </div>
  </div>
</template>

<script>
import Axios from 'axios'
import ShowCard from '../components/ShowCard'

export default {
  components: {
    ShowCard
  },
  data () {
    return {
      listId: this.$route.path.replace(/\//g, ''),
      listDetail: null,
      heroBackground: null,
      loggedInAs: null,
      loading: true
    }
  },
  beforeMount () {
    const path = this.$route.path
    Axios
      .get('http://localhost:5000/get/'.concat(encodeURI(path.replace(/\//g, ''))))
      .then(response => (this.listDetail = JSON.parse(response.data)))
    this.loading = false
  },
  mounted () {
    if (this.$cookies.get('token')) {
      const jwtCookie = this.$cookies.get('token')
      const decodedJwt = JSON.parse(atob(jwtCookie.split('.')[1]))
      this.loggedInAs = decodedJwt.identity
    }
  }
}
</script>

<style scoped>
.title-container {
  margin: 25px;
}
.title-cards {
  padding: 15px;
}
.big {
  text-align: center;
  font-size: 72px;
}
.add {
  text-align:center;
}
</style>
