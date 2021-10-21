<template>
  <l-map
    ref="map"
    style="height: 100%; position: relative; z-index: 1"
    :zoom="startZoom"
    :center="center"
    @update:bounds="update"
    @update:zoom="onZoom"
  >
    <l-control-layers position="bottomleft"></l-control-layers>
    <l-tile-layer ref="tileLayer" :url="url" :attribution="attribution"></l-tile-layer>
    <l-layer-group ref="circles" :visible='false' name="Плотность спортивных объектов" layer-type="base">
      <l-circle
          v-for="item in facilities"
          :key="'c' + item.id"
          :lat-lng="item.placement.coordinates"
          :radius="getRadius(item.availability)"
          :fillColor="isSquareCircleGreen(item.square) ? 'green': 'red'"
          :weight="0"
          :color="isSquareCircleGreen(item.square) ? 'green': 'red'"
          :opacity="0.45"
          :fillOpacity="getSquareCircleOpacity(item.square)"
          :interactive="false"
      />
    </l-layer-group>
    
    <hexes-layer-group name="Плотность населения" :hexes="hexes" :isBigHexes="isBigHexes"></hexes-layer-group>

    <l-marker v-if="selectedFacility" :lat-lng="selectedFacility.placement.coordinates" :icon="icon">
    </l-marker>


  </l-map>
</template>

<script>
import {LMap, LTileLayer, LMarker, LControlLayers, LLayerGroup,} from 'vue2-leaflet';
import L from "leaflet";
import icon from "../icon.png";
import "leaflet.markercluster/dist/leaflet.markercluster-src"
import HexesLayerGroup from './HexesLayerGroup.vue';

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LControlLayers,
    LLayerGroup,
    HexesLayerGroup,
  },
  computed: {
    facilities() {
      return this.$store.getters.newFacilities;
    },
    selectedFacility() {
      return this.$store.getters.selectedFacility;
    },
    facilityFilter() {
      return this.$store.getters.facilityFilter;
    },
    facilityReport() {
      return this.$store.getters.facilityReport;
    },
    maxOpacityPerFacility() {
      if (this.$store.getters.facilities.length > 1000) return 0.07;
      if (this.$store.getters.facilities.length > 500) return 0.12;
      return 0.3
    },
    hexes() {
      if (this.isBigHexes) return this.$store.getters.big_hexes;
      return this.$store.getters.small_hexes;
    }
  },
  watch: {
    selectedFacility(newVal) {
      if (!newVal) return;
      this.center = newVal.placement.coordinates;
    },
    facilityFilter(newVal) {
      this.markers.clearLayers()
      this.$store.commit("CLEAR_TILE_LIST")
      this.$store.commit('CLEAR_NEW_FACILITIES_BUFFER')
      this.$store.dispatch(
        "getFacilitiesByTiles",
        {
          tiles: this.bbox2tiles(this.boundsToBbox(this.bounds), this.getZoomForTiles()),
          facilityFilter: newVal
        }
      )
    },
    facilities(fac) {
      if (!fac.length) return;
      fac.forEach(el => {
        let marker = L.marker(L.latLng(el.placement.coordinates));
        this.markers.addLayer(marker)
      });
      this.$refs.circles.mapObject.addLayer(this.markers)
      this.$store.commit('CLEAR_NEW_FACILITIES_BUFFER')     
    },

  },
  data () {
    return {
      markers: L.markerClusterGroup({ chunkedLoading: true, disableClusteringAtZoom: 14, removeOutsideVisibleBounds: true}),
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      startZoom: 14,
      zoom: 14,
      center: [55.751244, 37.618423],
      isBigHexes: false,
      bounds: null,
      icon: L.icon({
        iconUrl: icon,
        popupAnchor: [1,-35],
        className: "selected",
      }),
      redSquareWeights: [
        60.0, 140.0, 256.0, 420.0, 686.5
      ],
      greenSquareWeights: [
        686.5, 1092.0, 1720.0, 2734.8, 4956.0, 5000000.0
      ],
      zoomBorder: 14,
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
      return opacity * this.maxOpacityPerFacility
    },
    isSquareCircleGreen: function (square) {
      return square > this.greenSquareWeights[0]
    },
    update: function (bounds) {
      this.bounds = bounds;
      this.$store.dispatch("getSmallHexes", {tiles: this.bbox2tiles(this.boundsToBbox(bounds), 13)})
      this.$store.dispatch(
          "getFacilitiesByTiles",
          {
            tiles: this.bbox2tiles(this.boundsToBbox(bounds), this.getZoomForTiles()),
            facilityFilter: this.$store.getters.facilityFilter
          }
      )
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
    },
    getZoomForTiles() {
      return 13
    },
    getFacilityReport(id) {
      this.$store.dispatch("getFacilityReport",{ id })
    },
    getAvailabilityNameById(id) {
      return this.$store.getters.availabilities.find( item => item.id === id)
    },
    getSportsNameById(ids) {
      let res = "";
      ids.forEach( id => {
        res += this.$store.getters.sportTypes.find((sport) => sport.id === id).name + " "
      })
      return res
    },
    getAreaTypeById(id) {
      return this.$store.getters.areaTypes.find( item => item.id === id)
    },
  },
  mounted() {
    // initial hexes
    // if (!this.$store.getters.small_hexes.length) {
    //   this.$store.dispatch(
    //       "getSmallHexes",
    //       {tiles: this.bbox2tiles([55.729188403516886, 37.54363059997559, 55.77324203759852, 37.693748474121094], 13)}
    //   )
    // }
    // if (!this.$store.getters.big_hexes.length) {
    //   this.$store.dispatch("getBigHexes");
    // }
    this.update(this.$refs.map.mapObject.getBounds())
  }
}
</script>

<style >
@import "~leaflet.markercluster/dist/MarkerCluster.css";
@import "~leaflet.markercluster/dist/MarkerCluster.Default.css";
@import url("https://unpkg.com/leaflet@1.0.0/dist/leaflet.css");

.selected {
  filter: hue-rotate(265deg);
  margin-left: -12px;
  margin-top: -41px;
}
</style>
