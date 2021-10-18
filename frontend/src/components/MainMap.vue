<template>
  <l-map
    style="height: 100%; position: relative; z-index: 1"
    :zoom="startZoom"
    :center="center"
    @update:bounds="update"
    @update:zoom="onZoom"
  >
    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
    <v-marker-cluster :options="{chunkedLoading: true, disableClusteringAtZoom: 14}">
      <template v-for="item in facilities">
        <l-marker v-if="!selectedFacility || item.id !== selectedFacility.id" :lat-lng="item.placement.coordinates" :key="item.id" @click="()=>getFacilityReport(item.id)" >
          <l-popup>
              <p>Name: {{facilityReport.name}} </p>
                <p>Availability: {{getAvailabilityNameById(facilityReport.availability).name}} </p>
                <p>Department: {{facilityReport.department.name}} </p>
               <p>Sports areas: </p>
               <div v-for="area in facilityReport.areas" :key="area.id">
                  <div class='text-body-2'>
                   &emsp; Name: {{area.name}} 
                  </div>
                  <div class='text-body-2'>
                    &emsp;&emsp; Sports: {{getSportsNameById(area.sports)}} 
                  </div>
                  <div class='text-body-2'>
                    &emsp;&emsp; Type: {{getAreaTypeById(area.type).name}}                     
                  </div>
                </div>            
          </l-popup>
        </l-marker>
      </template>
    </v-marker-cluster>
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
    <l-marker v-if="selectedFacility" :lat-lng="selectedFacility.placement.coordinates" :icon="icon">
    </l-marker>


  </l-map>
</template>

<script>
import {LMap, LTileLayer, LMarker, LCircle, LPopup} from 'vue2-leaflet';
import L from "leaflet";
import icon from "../icon.png";
import Vue2LeafletMarkerCluster from "vue2-leaflet-markercluster";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LCircle,
    LPopup,
    "v-marker-cluster": Vue2LeafletMarkerCluster
  },
  computed: {
    facilities() {
      return this.$store.getters.facilities;
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
    }
  },
  watch: {
    selectedFacility(newVal) {
      if (!newVal) return;
      this.center = newVal.placement.coordinates;
    },
    facilityFilter(newVal) {
      this.$store.dispatch(
        "getFacilitiesByTiles",
        {
          tiles: this.bbox2tiles(this.boundsToBbox(this.bounds), this.getZoomForTiles()),
          facilityFilter: newVal
        }
      )
    },
  },
  data () {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      startZoom: 14,
      zoom: 14,
      center: [55.751244, 37.618423],
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
      zoomBorder: 14
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
      this.$store.dispatch(
          "getFacilitiesByTiles",
          {
            tiles: this.bbox2tiles(this.boundsToBbox(bounds), this.getZoomForTiles()),
            facilityFilter: this.$store.getters.facilityFilter
          }
      )
    },
    onZoom: function (zoom) {
      this.zoom = zoom
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
      return this.zoom > 13? 13: 12
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
        res += this.$store.getters.sportTypes.find((sport) => sport.id == id).name + " "
      })
      return res
    },
    getAreaTypeById(id) {
      return this.$store.getters.areaTypes.find( item => item.id === id)
    },
  }
}
</script>

<style >
@import "~leaflet/dist/leaflet.css";
@import "~leaflet.markercluster/dist/MarkerCluster.css";
@import "~leaflet.markercluster/dist/MarkerCluster.Default.css";

.selected {
  filter: hue-rotate(265deg);
  margin-left: -12px;
  margin-top: -41px;
}
</style>
