<template>
  <l-map
    ref="map"
    style="height: 100%; position: relative; z-index: 1"
    :zoom="startZoom"
    :center="center"
    @update:bounds="update"
    @update:zoom="onZoom"
    @overlayadd="overlayadd"
    @overlayremove="overlayremove"
    @baselayerchange="baselayerchange"
    :options="{zoomControl: false}"
  >
    <l-control-zoom position="bottomright"></l-control-zoom>
    <l-control position="topright" >
      <v-btn-toggle multiple class="selectBtn" >
        <v-btn @click='handleLayerControl' >
          <v-icon small>mdi-layers-triple-outline</v-icon>
        </v-btn>        
        <v-btn @click='canSelect = !canSelect' :disabled="baseLayer && baseLayer.name !== layerNames[3]">
          <v-icon small>mdi-select-multiple</v-icon>
        </v-btn>
      </v-btn-toggle>
    </l-control>
    <l-control-layers ref="control" :collapsed="false" position="topright"></l-control-layers>
    <l-control v-if="selectedHexes.length" position="topright">
      <v-btn  
        :to="{ path: `/report/${isBigHexes}/${JSON.stringify(selectedHexes)}`}"
        target="_blank" 
        depressed 
        fab
        height="40px"
        width="40px"
        class="mr-2"
        >
          <v-icon>mdi-chart-line</v-icon>
        </v-btn>
    </l-control>


    <l-tile-layer ref="tileLayer" :url="url" :attribution="attribution"></l-tile-layer>
    <l-layer-group ref="circles" :visible='true' :name="layerNames[0]" layer-type="overlay">
    </l-layer-group>
    <l-layer-group
      name='Отключено'
      layer-type="base"
      :visible='true'
    ></l-layer-group>
    <hexes-layer-group 
      :name="layerNames[1]" 
      :hexes="baseLayer && baseLayer.name === layerNames[1]? hexes : []"
      :colormap="[{index: 0, rgb:[255,0,0]},{index: 0.5, rgb: [255,125,125]},{index: 1, rgb: [255,255,255]}]" 
      color="red" 
      :canSelect='canSelect'
      :bins="isBigHexes? populationBigHexBins : populationSmallHexBins" 
      opacityBy="population" 
      layerType="base"
      >
        <template v-slot:popup="{prop}">
          <p>Population: {{Math.round(prop.population)}}</p>
          <p>Density: {{ isBigHexes? Math.round( prop.population / 0.7373) : Math.round( prop.population / 0.105)}}</p>
        </template>
    </hexes-layer-group>

    <hexes-layer-group 
      :name="layerNames[2]" 
      :hexes="baseLayer && baseLayer.name === layerNames[2]? hexes : []"
      colormap="greens" 
      color="green" 
      :bins="isBigHexes? sportBigHexBins : sportSmallHexBins"  
      :canSelect='canSelect'
      opacityBy="square" 
      layerType="base">
        <template v-slot:popup="{prop}">
          <p>Areas count: {{prop.areas_count }}</p>
          <p>Square: {{ Math.round(prop.square) }}</p>
        </template>
    </hexes-layer-group>

    <hexes-layer-group 
      :name="layerNames[3]" 
      :hexes="baseLayer && baseLayer.name === layerNames[3]? hexes : []"
      colormap="greens" 
      color="green" :bins="isBigHexes? unitingBigHexBins : unitingSmallHexBins"  
      :canSelect='canSelect'
      opacityBy="square_by_person" 
      layerType="base">
      <template v-slot:popup="{prop}">
        <p>Areas count: {{ prop.areas_count }}</p>
        <p>Square: {{ Math.round(prop.square) }}</p>
        <p>Square by person: {{ Math.round(prop.square_by_person) }}</p>
      </template>
    </hexes-layer-group>
  </l-map>
</template>

<script>
import {LMap, LTileLayer, LControlLayers, LLayerGroup,LControlZoom, LControl} from 'vue2-leaflet';
import L from "leaflet";
import icon from "../icon.png";
import "leaflet.markercluster/dist/leaflet.markercluster-src"
import HexesLayerGroup from './HexesLayerGroup.vue';

export default {
  components: {
    LMap,
    LTileLayer,
    LControlLayers,
    LControlZoom,
    LControl,
    LLayerGroup,
    HexesLayerGroup,
  },
  computed: {
    console: ()=> console,
    selectedHexes(){
      return this.$store.getters.selectedHexes;
    },
    facilities() {
      return this.$store.getters.newFacilities;
    },
    selectedFacility() {
      return this.$store.getters.selectedFacility;
    },
    facilityFilter() {
      return this.$store.getters.facilityFilter;
    },
    sportFilter() {
      return this.$store.getters.sportFilter;
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
      return this.$store.getters.hexes;
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
      if (!newVal) return
      this.$store.dispatch(
        "getFacilitiesByTiles",
        {
          tiles: this.bbox2tiles(this.boundsToBbox(this.bounds), this.getZoomForTiles()),
          facilityFilter: newVal
        }
      )
    },
    sportFilter() {
      this.$store.commit("CLEAR_HEXES")
      this.$store.commit("CLEAR_LAST_DENSITY_TILES")
      this.$store.commit("CLEAR_SELECTED_HEXES")
      this.update(this.$refs.map.mapObject.getBounds())
    },
    facilities(fac) {
      if (!fac.length) return;
      fac.forEach(el => {
        let marker = L.marker(L.latLng(el.placement.coordinates));
        marker.on('click', () => this.showInformation(el))
        marker.bindTooltip(el.name)
        this.markers.addLayer(marker)
      });
      this.$refs.circles.mapObject.addLayer(this.markers)
      this.$store.commit('CLEAR_NEW_FACILITIES_BUFFER')
    },

  },
  data () {
    return {
      markers: L.markerClusterGroup({ chunkedLoading: true, disableClusteringAtZoom: 14, removeOutsideVisibleBounds: true}),
      url: 'http://tile2.maps.2gis.com/tiles?x={x}&y={y}&z={z}',
      attribution:
        '&copy; <a target="_blank" href="http://law.2gis.ru/api-rules/">2GIS</a> contributors',
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
      layerNames: ["Спортивные объекты","Плотность населения","Плотность спортивных объектов","Объединение населения и объектов"],
      zoomBorder: 14,
      activeLayers: [],
      baseLayer: null,
      canSelect: false,
      unitingBigHexBins: [4, 6, 9, 13, 18, 27, 45, 114, 681, 2928, 11948, 48660],
      unitingSmallHexBins: [51, 81, 236, 3016, 8978, 22328, 34320, 43541, 54268, 63705, 100283, 111083],
      populationBigHexBins: [27, 379, 1900, 6627, 11525, 17106, 23040, 26530, 43127],
      populationSmallHexBins: [5, 22, 360, 1597, 2661, 3805, 4739, 5333, 11000],
      sportSmallHexBins: [124, 6866, 26184, 64665, 94201, 118899, 140914, 167049, 192377, 238084, 300000],
      sportBigHexBins: [144,6520,27080,64477,95195,119351,142339,167483,193332,238483,445060]
    };
  },
  methods: {
    handleLayerControl(){
      const classes = this.$el.querySelector('.leaflet-control-layers').classList;
      if (classes.contains('hide')) {
        classes.remove('hide')
      } else {
        classes.toggle('hide')
      }
    },
    showInformation(facility){
      console.log(facility.id);
      this.$store.dispatch('getFacilityReport', facility)
    },
    baselayerchange: function(layer) {
      this.baseLayer = layer
      this.$store.commit("CLEAR_HEXES")
      this.$store.commit("CLEAR_LAST_DENSITY_TILES")
      this.$store.commit("CLEAR_SELECTED_HEXES")
      this.update(this.$refs.map.mapObject.getBounds())
    },
    overlayadd: function(overlay){
      this.activeLayers.push(overlay)
      this.$store.commit("SET_SELECTED_FACILITY_LAYER",true)
      this.update(this.$refs.map.mapObject.getBounds())
    },
    overlayremove: function(overlay){
      this.activeLayers.splice(this.activeLayers.indexOf(overlay),1)  
      this.$store.commit("SET_SELECTED_FACILITY_LAYER",false)
      this.update(this.$refs.map.mapObject.getBounds())
    },
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
      let tiles = this.bbox2tiles(this.boundsToBbox(bounds), this.getZoomForTiles())
      if (this.facilityFilter) {
        this.$store.dispatch(
          "getFacilitiesByTiles",
          {
            tiles,
            facilityFilter: this.$store.getters.facilityFilter
          }
        )
      }

      switch (this.baseLayer?.name) {
        case this.layerNames[1]:
          if (this.isBigHexes) {
            this.$store.dispatch("getDensityBigHexes",{tiles});
          } else {
            this.$store.dispatch("getDensitySmallHexes", {tiles})
          }
          break;
        case this.layerNames[2]:
          if (this.isBigHexes) {
            this.$store.dispatch("getSportBigHexes",{tiles});
          } else {
            this.$store.dispatch("getSportSmallHexes", {tiles})
          }
          break;
        case this.layerNames[3]:
          if (this.isBigHexes) {
            this.$store.dispatch("getUnitingBigHexes",{tiles});
          } else {
            this.$store.dispatch("getUnitingSmallHexes", {tiles})
          }
          break;
        default:
          break;
      }  
    },
    onZoom: function (zoom) {
      if (this.isBigHexes && zoom >= 14) {
        this.isBigHexes = false;
        this.$store.commit("CLEAR_SELECTED_HEXES")
      } else if (!this.isBigHexes && zoom < 14) {
        this.isBigHexes = true;
        this.$store.commit("CLEAR_SELECTED_HEXES")
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
    this.$nextTick(() => {
      this.update(this.$refs.map.mapObject.getBounds());

      this.handleLayerControl()
    })
  }
}

</script>

<style >
@import "~leaflet.markercluster/dist/MarkerCluster.css";
@import "~leaflet.markercluster/dist/MarkerCluster.Default.css";
@import url("https://unpkg.com/leaflet@1.0.0/dist/leaflet.css");
.icon{
  min-width: 44px !important;
}
.selectBtn {
  border: 2px solid rgba(0,0,0,0.2);
  border-radius: 20px !important;
  margin-right: 10px !important;
}
.selected {
  filter: hue-rotate(265deg);
  margin-left: -12px;
  margin-top: -41px;
}
.leaflet-control-layers{
  /* display: none; */
  margin-right: 20px !important;
  border-radius: 20px !important;
}
.hide{
  display: none;
}
.leaflet-control-layers-overlays{
  padding: 5px;
}
.leaflet-control-zoom{
  margin-bottom: 20px !important;
  margin-right: 20px !important;
  border: 0px !important;
}
.leaflet-control-zoom-in{
  width: 40px !important;
  height: 40px !important;
  border-top-left-radius: 20px !important;
  border-top-right-radius: 20px !important;
}
.leaflet-control-zoom-out{
  width: 40px !important;
  height: 40px !important;
  border-bottom-left-radius: 20px !important;
  border-bottom-right-radius: 20px !important;
}
</style>
