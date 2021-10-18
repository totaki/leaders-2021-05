<template>
  <div id="app">
    <MainMap/>
    <MainMenu/>
  </div>
</template>

<script>
import MainMap from './components/MainMap.vue'
import MainMenu from './components/MainMenu'

export default {
  name: 'App',
  components: {
    MainMap,
    MainMenu
  },
  async mounted() {
    this.$store.dispatch("getDepartments")
    this.$store.dispatch("getAreaTypes")
  }
}
</script>

<style>
body, html {
  height: 100%;
  width: 100%;
}

body {
  margin: 0;
}

#app {
  width: 100%;
  height: 100%;
}
</style>
