<template>
    <l-layer-group ref="layer" :visible='false' :name="name" :layer-type="layerType" :options='options'>
<!--        <l-polygon-->
<!--          v-for="poly in hexes"-->
<!--          :lat-lngs="poly.polygon.coordinates[0]"-->
<!--          :key="poly.id"-->
<!--          :fillColor="getColorMap(poly[opacityBy],bins)"-->
<!--          :fillOpacity="0.7"-->
<!--          :weight="1"-->
<!--          :color="getSelected.find(hex => hex===poly.id)? 'red' : ''"-->
<!--          @click="canSelect && selectHex(poly)"-->
<!--          >-->
<!--          <l-popup>-->
<!--            <slot name="popup" v-bind:prop="poly"></slot>-->
<!--          </l-popup>-->
<!--        </l-polygon>-->
    </l-layer-group>
</template>
<script>
// import { LPolygon, LLayerGroup, LPopup  } from 'vue2-leaflet';
import { LLayerGroup  } from 'vue2-leaflet';
import Colormap from 'colormap';
import L from "leaflet";

export default {
    props:{
        hexes:{},
        isBigHexes:{},
        name:{},
        canSelect:{default: false,type: Boolean},
        'layer-type': {default: 'base',type: String},
        options:{},
        opacityBy:{},
        bins:{},
        color:{},
        colormap:{},
    },
    components: {
        // LPolygon,
        LLayerGroup,
        // LPopup
    },
    computed:{
        console: () => console,
        getSelected: function() {return this.$store.getters.selectedHexes}
    },
    watch: {
        hexes: function (newVal) {
            if (!newVal) return;
            this.$refs.layer.mapObject.removeLayer(this.hexArray)
            this.hexArray.clearLayers();
            newVal.forEach(el => {
                let options ={
                    fillColor: this.getColorMap(el[this.opacityBy],this.bins),
                    fillOpacity: 0.7,
                    weight: 1,
                    color: this.getSelected.find(hex => hex === el.id)? 'red' : ''
                }
                let hex = L.polygon(el.polygon.coordinates[0],options);
                this.hexArray.addLayer(hex)
            });
            this.$refs.layer.mapObject.addLayer(this.hexArray)
        }
    },
    data() {
        return {
            hexArray: L.layerGroup(),
            selected: []
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
        selectHex(hex){
            this.$store.dispatch("getSelectedHexes",hex.id)
        }
    },
}
</script>
<style scoped>
    
</style>