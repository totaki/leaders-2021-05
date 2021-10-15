<template>
  <div id="app">
    <MainMap/>
  </div>
</template>

<script>
import MainMap from './components/MainMap.vue'

export default {
  name: 'App',
  components: {
    MainMap
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
