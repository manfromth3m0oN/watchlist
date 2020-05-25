<template>
  <div v-if="listDetail">
  <div v-if="listDetail.owner === loggedInAs">
        <section class="hero is-primary">
        <div class="hero-body">
          <div class="container">
            <div class="columns">
              <div class="column is-10">
                <h1 class="title">
                  {{ listId }}
                </h1>
                <h3 class="subtitle" v-if="listDetail">
                  Created by: {{ listDetail.owner }}
                </h3>
              </div>
            </div>
          </div>
        </div>
    </section>
    <div class="title-container">
      <EditCard
        class="title-cards"
        v-for="(watched, movTitle) in listDetail.titles"
        :key="movTitle"
        :title="movTitle"
        :list="listId"
        :watched="watched"
      />
    </div>
  </div>
  <div v-else>
    <section class="hero is-danger is-medium">
  <div class="hero-body">
    <div class="container">
      <h1 class="title">
        You do not have the correct authorization to view this page
      </h1>
    </div>
  </div>
</section>
  </div>
  </div>
</template>

<script>
import Axios from 'axios'
import EditCard from '../../components/EditCard'

export default {
  components: {
    EditCard
  },
  data () {
    return {
      listId: this.$route.path.replace(/\/edit\//g, ''),
      listDetail: null,
      loggedInAs: null
    }
  },
  mounted () {
    const path = this.$route.path.replace(/\/edit\//g, '')
    Axios
      .get('http://localhost:5000/get/'.concat(encodeURI(path)))
      .then(response => (this.listDetail = JSON.parse(response.data)))
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
</style>
