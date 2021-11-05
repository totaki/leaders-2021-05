<template>
    <l-layer-group ref="layer" :visible='false' :name="name" :layer-type="layerType" :options='options'>

    </l-layer-group>
</template>
<script>
import { LLayerGroup  } from 'vue2-leaflet';
import L from "leaflet";

export default {
    props:{
        hexes:{},
        isBigHexes:{},
        name:{},
        canSelect:{default: true,type: Boolean},
        canMultiSelect:{default: false,type: Boolean},
        'layer-type': {default: 'base',type: String},
        options:{},
        opacityBy:{},
        bins:{},
        color:{},
        colormap:{},

    },
    components: {
        LLayerGroup,
    },
    computed:{
        console: () => console,
        getSelected: function() {return this.$store.getters.selectedHexes}
    },
    watch: {
        hexes: function (newVal) {
            if (!newVal) return;
            this.lastSelected = null
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
                hex.on('click',()=> this.canSelect && this.selectHex(hex,el))
                this.hexArray.addLayer(hex)
            });
            this.$refs.layer.mapObject.addLayer(this.hexArray)
        }
    },
    data() {
        return {
            hexArray: L.layerGroup(),
            lastSelected: null
        }
    },
    methods: {
        getColorMap: function (opacityBy,bins) {
            let colorIdx = bins.findIndex( bin => opacityBy < bin)

            return colorIdx === -1? this.colormap[this.colormap.length - 1] : this.colormap[colorIdx]
        },
        selectHex(hex,hexPoly){
            if (this.canMultiSelect) {
                if (!this.getSelected.find(hex => hex === hexPoly.id)) {
                    hex.setStyle({color: 'red'})
                    this.$store.dispatch("getSelectedHexes", [{hexPoly,hex}, ...this.getSelected])
                } else {
                    hex.setStyle({color: ''})
                    this.$store.dispatch("getSelectedHexes", this.getSelected.filter(el => el.hexPoly.id !== hexPoly.id))
                }
            } else {
                if (this.getSelected.length > 1) {
                    this.getSelected.forEach( el => {
                        el.hex.setStyle({color:''})
                    })
                    this.$store.dispatch("getSelectedHexes",[])
                }
                if (this.lastSelected === hex) {
                    hex.setStyle({color: ''})
                    this.lastSelected = null
                    this.$store.dispatch("getSelectedHexes",[])
                } else {
                    hex.setStyle({color: 'red'})
                    this.lastSelected?.setStyle({color: ''})
                    this.lastSelected = hex
                    this.$store.dispatch("getSelectedHexes",[{hexPoly,hex}])
                }
            }
        }
    },
}
</script>
<style scoped>
    
</style>