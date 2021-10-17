<template>
  <l-map
    style="height: 100%; position: relative; z-index: 1"
    :zoom="zoom"
    :center="center"
  >
    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
    <div v-for="item in facilities" :key="item.id">
      <l-marker v-if="!selectedFacility || item.id !== selectedFacility.id" :lat-lng="item.placement.coordinates" />
    </div>
    <l-marker v-if="selectedFacility" :lat-lng="selectedFacility.placement.coordinates" :icon="icon"/>
  </l-map>
</template>

<script>
import {LMap, LTileLayer, LMarker} from 'vue2-leaflet';
import L from "leaflet";
import icon from "../icon.png";
export default {
  components: {
    LMap,
    LTileLayer,
    LMarker
  },
  computed: {
    facilities() {
      return this.$store.getters.facilities;
    },
    selectedFacility() {
      return this.$store.getters.selectedFacility;
    },
  },
  watch: {
    selectedFacility(newVal) {
      if (!newVal) return;
      this.center = newVal.placement.coordinates;
    },
  },
  data () {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 14,
      center: [55.751244, 37.618423],
      icon: L.icon({
        iconUrl: icon,
        className: "selected",
      }),
    };
  }
}
</script>

<style >
@import "~leaflet/dist/leaflet.css";
.selected {
  filter: hue-rotate(265deg);
  margin-left: -12px;
    margin-top: -41px;
    z-index: 394 !important;
}
</style>
