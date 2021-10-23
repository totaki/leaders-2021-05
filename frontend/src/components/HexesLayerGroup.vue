<template>
    <l-layer-group :visible='false' :name="name" :layer-type="layerType" :options='options'>
        <l-polygon
          v-for="poly in hexes"
          :lat-lngs="poly.polygon.coordinates[0]"
          :key="poly.id"
          :fillColor="getColorMap(poly[opacityBy],bins)"
          :fillOpacity="0.7"
          :weight="0">
          <l-popup>
            <slot name="popup" v-bind:prop="poly"></slot>
          </l-popup>
        </l-polygon>
    </l-layer-group>
</template>
<script>
import { LPolygon, LLayerGroup, LPopup  } from 'vue2-leaflet';
import Colormap from 'colormap';

export default {
    props:['hexes','isBigHexes','name','layerType','options','opacityBy','bins','color','colormap'],
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
        getColorMap: function (opacityBy,bins) {
            let colors = Colormap({
                colormap: this.colormap,
                nshades: bins.length,
                format: 'hex',
                alpha: 1}).reverse();
            let colorIdx = bins.findIndex( bin => opacityBy < bin)

            return colorIdx === -1? colors[colors.length - 1] : colors[colorIdx]
        },
    },
}
</script>
<style scoped>
    
</style>