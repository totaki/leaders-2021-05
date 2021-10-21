<template>
    <l-layer-group :visible='false' :name="name" layer-type="base">
      <l-polygon
          v-for="poly in hexes"
          :lat-lngs="poly.polygon.coordinates[0]"
          :key="poly.id"
          fillColor="red"
          :fillOpacity="getOpacity(poly.population)"
          :weight="0">
          <l-popup>
            <p>Population: {{Math.round(poly.population)}}</p>
            <p>Density: {{ isBigHexes? Math.round( poly.population * 0.85) : Math.round( poly.population * 0.1)}}</p>
          </l-popup>
      </l-polygon>
    </l-layer-group>
</template>
<script>
import { LPolygon, LLayerGroup, LPopup  } from 'vue2-leaflet';

export default {
    props:['hexes','isBigHexes','name'],
    components: {
        LPolygon,
        LLayerGroup,
        LPopup
    },
    computed:{
        console: () => console
    },
    created() {

    },
    watch: {

    },
    data() {
        return {
            bigHexBins: [27, 379, 1900, 6627, 11525, 17106, 23040, 26530, 43127],
            smallHexBins: [5, 22, 360, 1597, 2661, 3805, 4739, 5333, 11000],
        }
    },
    methods: {
        getOpacity: function (population) {
            let opacity = 0;
            for (const val of (this.isBigHexes ? this.bigHexBins : this.smallHexBins)) {
                opacity += 0.1
                if (population < val) break;
            }
            return opacity * 0.7
    },
    },
}
</script>
<style scoped>
    
</style>