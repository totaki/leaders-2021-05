<template>
  <v-app>
    <MainMenu />
    <v-main>
      <MainMap />
    </v-main>
  </v-app>
</template>
<script>
import MainMap from "./MainMap";
import MainMenu from "./MainMenu";

export default {
  components: {
    MainMap,
    MainMenu,
  },
  async mounted() {
    this.$store.dispatch("getDepartments");
    this.$store.dispatch("getAreaTypes");
    this.$store.dispatch("getSportTypes");
  },
};
</script>
<style >

</style>