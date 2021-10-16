<template>
  <l-map
      style="height: 100%; position: relative; z-index: 1"
      :zoom="zoom"
      :center="center"
      @update:bounds="update"
      @update:zoom="onZoom"
  >
    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
    <l-polygon
        v-for="poly in hexes"
        :lat-lngs="poly.polygon.coordinates[0]"
        :key="poly.id"
        fillColor="red"
        :fillOpacity="getOpacity(poly.population)"
        :interactive="false"
        :weight="0">
    </l-polygon>
  </l-map>
</template>

<script>
import {LMap, LPolygon, LTileLayer} from 'vue2-leaflet';

export default {
  components: {
    LMap,
    LTileLayer,
    LPolygon,
  },
  data() {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
          '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 14,
      center: [55.751244, 37.618423],
      bigHexBins: [27, 379, 1900, 6627, 11525, 17106, 23040, 26530, 43127],
      smallHexBins: [5, 22, 360, 1597, 2661, 3805, 4739, 5333, 11000],
      isBigHexes: false,
      bounds: null
    };
  },
  methods: {
    update: function (bounds) {
      this.bounds = bounds;
      this.$store.dispatch("getSmallHexes", {tiles: this.bbox2tiles(this.boundsToBbox(bounds), 13)})
    },
    onZoom: function (zoom) {
      if (this.isBigHexes && zoom >= 14) {
        this.isBigHexes = false;
        // this.$store.dispatch("getSmallHexes", {bbox: this.boundsToBbox(this.bounds)});
      } else if (!this.isBigHexes && zoom < 14) {
        this.isBigHexes = true;
      }
    },
    getOpacity: function (population) {
      let opacity = 0;
      for (const val of (this.isBigHexes ? this.bigHexBins : this.smallHexBins)) {
        opacity += 0.1
        if (population < val) break;
      }
      return opacity * 0.7
    },
    boundsToBbox: function (bounds) {
      return [bounds._southWest.lat, bounds._southWest.lng, bounds._northEast.lat, bounds._northEast.lng]
    },
    lon2tile: function (lon, zoom) {
      return (Math.floor((lon + 180) / 360 * Math.pow(2, zoom)));
    },
    lat2tile: function (lat, zoom) {
      return (Math.floor((1 - Math.log(Math.tan(lat * Math.PI / 180) + 1 / Math.cos(lat * Math.PI / 180)) / Math.PI) / 2 * Math.pow(2, zoom)));
    },
    tile2long: function (x, z) {
      return (x / Math.pow(2, z) * 360 - 180);
    },
    tile2lat: function (y, z) {
      const n = Math.PI - 2 * Math.PI * y / Math.pow(2, z);
      return (180 / Math.PI * Math.atan(0.5 * (Math.exp(n) - Math.exp(-n))));
    },
    bbox2tiles: function (bbox, zoom) {
      const y1 = this.lat2tile(bbox[1], zoom);
      const x1 = this.lon2tile(bbox[0], zoom);
      const y2 = this.lat2tile(bbox[3], zoom);
      const x2 = this.lon2tile(bbox[2], zoom);
      let tiles = []
      for (let i = Math.min(y1, y2); i <= Math.max(y1, y2); i++) {
        for (let j = Math.min(x1, x2); j <= Math.max(x1, x2); j++) {
          tiles.push([j, i, zoom])
        }
      }
      return tiles
    }
  },
  computed: {
    hexes() {
      if (this.isBigHexes) return this.$store.getters.big_hexes;
      return this.$store.getters.small_hexes;
    }
  },
  mounted() {
    // initial hexes
    if (!this.$store.getters.small_hexes.length) {
      this.$store.dispatch(
          "getSmallHexes",
          {tiles: this.bbox2tiles([55.729188403516886, 37.54363059997559, 55.77324203759852, 37.693748474121094], 13)}
      )
    }
    if (!this.$store.getters.big_hexes.length) {
      this.$store.dispatch("getBigHexes");
    }
  }
}
</script>

<style scoped>
@import "~leaflet/dist/leaflet.css";
</style>
