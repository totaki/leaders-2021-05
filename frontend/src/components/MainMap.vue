<template>
  <l-map
    style="height: 100%; position: relative; z-index: 1"
    :zoom="zoom"
    :center="center"
  >
    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
    <template v-for="item in facilities">
      <l-marker v-if="!selectedFacility || item.id !== selectedFacility.id" :lat-lng="item.placement.coordinates" :key="item.id" />
      <l-circle
          :key="'c' + item.id"
          :lat-lng="item.placement.coordinates"
          :radius="getRadius(item.availability)"
          :fillColor="isSquareCircleGreen(item.square) ? 'green': 'red'"
          :weight="1"
          :color="isSquareCircleGreen(item.square) ? 'green': 'red'"
          :opacity="0.45"
          :fillOpacity="getSquareCircleOpacity(item.square)"
          :interactive="false"
      />
    </template>
    <l-marker v-if="selectedFacility" :lat-lng="selectedFacility.placement.coordinates" :icon="icon"/>


  </l-map>
</template>

<script>
import {LMap, LTileLayer, LMarker, LCircle} from 'vue2-leaflet';
import L from "leaflet";
import icon from "../icon.png";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LCircle,
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
      redSquareWeights: [
        60.0, 140.0, 256.0, 420.0, 686.5
      ],
      greenSquareWeights: [
        686.5, 1092.0, 1720.0, 2734.8, 4956.0, 5000000.0
      ]
    };
  },
  methods: {
    getRadius: function (availability) {
      if (availability === 4) return 500;
      if (availability === 3) return 1000;
      if (availability === 2) return 3000;
      if (availability === 1) return 5000;
    },
    getSquareCircleOpacity: function (square) {
      let opacity = 0;
      if (this.isSquareCircleGreen(square)) {
        for (const weight of this.greenSquareWeights) {
          opacity += 0.2
          if (square <= weight) break;
        }
      } else {
        opacity = 1
        for (const weight of this.redSquareWeights) {
          opacity -= 0.18
          if (square < weight) break;
        }
      }
      if (opacity <= 0.01) console.log(`square ${square}`)
      return opacity * 0.4
    },
    isSquareCircleGreen: function (square) {
      return square > this.greenSquareWeights[0]
    }
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
