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

};
</script>
<style >

</style>