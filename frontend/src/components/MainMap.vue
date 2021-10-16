<template>
  <l-map style="height: 100%; position: relative; z-index: 1" :zoom="zoom" :center="center">
    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
    <div v-for="item in facilities" :key="item.id">
      <l-marker :lat-lng="item.placement.coordinates"/>
    </div>
  </l-map>
</template>

<script>
  import {LMap, LTileLayer, LMarker} from 'vue2-leaflet';

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker
  },
  computed: {
    facilities() {
      return this.$store.getters.facilities;
    }
  },
  data () {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 14,
      center: [55.751244, 37.618423],
    };
  }
}
</script>

<style scoped>
@import "~leaflet/dist/leaflet.css";
</style>
