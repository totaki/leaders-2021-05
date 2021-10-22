<template>
    <l-layer-group :visible='false' :name="name" :layer-type="layerType" :options='options'>
      <l-polygon
          v-for="poly in hexes"
          :lat-lngs="poly.polygon.coordinates[0]"
          :key="poly.id"
          :fillColor="color"
          :fillOpacity="getOpacity(poly[opacityBy],bins)"
          :weight="0">
          <l-popup>
            <slot name="popup" v-bind:prop="poly"></slot>
          </l-popup>
      </l-polygon>
    </l-layer-group>
</template>
<script>
import { LPolygon, LLayerGroup, LPopup  } from 'vue2-leaflet';

export default {
    props:['hexes','isBigHexes','name','layerType','options','opacityBy','bins','color'],
    components: {
        LPolygon,
        LLayerGroup,
        LPopup
    },
    computed:{
        console: () => console
    },
    created() {
        console.log(this.hexes);
    },
    watch: {

    },
    data() {
        return {
            
        }
    },
    methods: {
        getOpacity: function (population,bins) {
            let opacity = 0;
            for (const val of bins) {
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