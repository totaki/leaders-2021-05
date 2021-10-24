<template>
  <div id="app">
      <router-view />
  </div>
</template>

<script>

export default {
  name: 'App',
    async mounted() {
    this.$store.dispatch("getDepartments");
    this.$store.dispatch("getAreaTypes");
    this.$store.dispatch("getSportTypes");
  },
}
</script>

<style>
#app {
  width: 100%;
  height: 100%;
}
</style>
