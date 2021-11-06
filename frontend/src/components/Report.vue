<template>
    <v-app>
        <v-sheet
            color="white"
            elevation="1"
            width="1000"
            class="mx-auto mt-2 my-auto pa-6"
            v-if="hexReport"
        >
            <l-map style="height: 330px" :zoom="14" :center="center">
                <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
                <l-polygon ref="polygon" :lat-lngs="coordinates"></l-polygon>
            </l-map>
            <v-container class="px-14">
                <div class="text-h4 text-center pb-4">Информация по выбранным полигонам </div>
                <v-row class="pb-4">
                    <v-col
                        cols="6"
                    >
                        <v-card height="140">
                            <v-card-title>
                                Общая площадь полигонов
                            </v-card-title>
                            <v-card-text class="text-h3 primary--text">
                                {{hexReport.total_square.toFixed(3)}} км<sup>2</sup>
                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-col
                        cols="6"
                    >
                        <v-card height="140">
                            <v-card-title>
                                Суммарное население полигонов
                            </v-card-title>
                            <v-card-text class="text-h3 primary--text">
                                {{hexReport.total_population}} человек
                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-col
                        cols="6"
                    >
                        <v-card height="140">
                            <v-card-title>
                                Плотность населения
                            </v-card-title>
                            <v-card-text class="text-h3 primary--text">
                                {{ Math.round(hexReport.total_population / hexReport.total_square) }} чел/км<sup>2</sup>
                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-col
                        cols="6"
                    >
                        <v-card height="140">
                            <v-card-title>
                                Суммарная площадь спортобъектов
                            </v-card-title>
                            <v-card-text class="text-h3 primary--text">
                                {{Math.round(hexReport.total_sport_square)}} м<sup>2</sup>
                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-col
                        cols="6"
                    >
                        <v-card height="140">
                            <v-card-title>
                                Количество доступных видов спорта
                            </v-card-title>
                            <v-card-text class="text-h3 primary--text">
                                {{hexReport.sports.length}} из 160
                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-col
                        cols="6"
                    >
                        <v-card height="140">
                            <v-card-title>
                                Доступность типов спортивных зон
                            </v-card-title>
                            <v-card-text class="text-h3 primary--text">
                                {{Object.keys(this.hexReport.area_types_counter).length}} из 108
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
                <div class="text-h5 text-center py-4">Количество спортивных зон</div>
                <HorizontalBarChart :chartdata="sportAreasChartDataset"></HorizontalBarChart>
                <div class="text-h5 text-center py-4">Площадь спортивных зон на человека</div>
                <HorizontalBarChart :chartdata="sportAreasSquareChartDataset"></HorizontalBarChart>
                <div class="text-h5 text-center py-4">Детальная информация</div>
                <v-expansion-panels>
                    <v-expansion-panel>
                        <v-expansion-panel-header>
                            Список доступных видов спорта
                        </v-expansion-panel-header>
                        <v-expansion-panel-content>
                            <ul class="text-body-2 ml-4" v-for="sport in hexReport.sports" :key="sport">
                                <li>{{sportTypes.find( ar => ar.id === +sport).name}}</li>
                            </ul>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel>
                        <v-expansion-panel-header>
                            Суммарная площадь по типу спортивной зоны
                        </v-expansion-panel-header>
                        <v-expansion-panel-content>
                            <ul class="text-body-2 ml-4" v-for="area in Object.entries(hexReport.area_types_coverage)" :key="area[0]">
                                <li>{{areaTypes.find( ar => ar.id === +area[0]).name}}: {{Math.round(area[1])}} м<sup>2</sup></li>
                            </ul>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel>
                        <v-expansion-panel-header>
                            Количество спортивных зон
                        </v-expansion-panel-header>
                        <v-expansion-panel-content>
                            <ul class="text-body-2 ml-4" v-for="area in Object.entries(hexReport.area_types_counter)" :key="Math.random(area[0])">
                                <li>{{areaTypes.find( ar => ar.id === +area[0]).name}}: {{Math.round(area[1])}} шт.</li>
                            </ul>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                </v-expansion-panels>
            </v-container>
        </v-sheet>
    </v-app>

</template>
<script>
import HorizontalBarChart from "./charts/HorizontalBarChart";
import {LMap, LTileLayer, LPolygon} from 'vue2-leaflet';

export default {
    components: {
        LMap,
        LTileLayer,
        HorizontalBarChart,
        LPolygon
    },
    data () {
        return {
            url: 'http://tile2.maps.2gis.com/tiles?x={x}&y={y}&z={z}',
            attribution:
                '&copy; <a target="_blank" href="http://law.2gis.ru/api-rules/">2GIS</a> contributors',
            zoom: 15,
        }
    },
    computed: {
        hexReport(){
            return this.$store.getters.hexReport
        },
        areaTypes() {
            return this.$store.getters.areaTypes;
        },
        sportTypes() {
            if (!this.$store.getters.sportTypes) return []
            return this.$store.getters.sportTypes;
        },
        sportAreasChartDataset() {
            if (!this.hexReport) return;
            console.log(this.areaTypes)
            return {
                labels: Object.keys(this.hexReport.area_types_counter).map(type_id => this.areaTypes.find( ar => ar.id === +type_id).name),
                datasets: [
                    {
                        label: 'Количество спортивных зон',
                        backgroundColor: '#ec0e43',
                        data: Object.values(this.hexReport.area_types_counter)
                    },
                ]
            }
        },
        sportAreasSquareChartDataset() {
            if (!this.hexReport || !this.areaTypes) return;
            return {
                labels: Object.keys(this.hexReport.area_types_coverage).map(type_id => this.areaTypes.find( ar => ar.id === +type_id).name),
                datasets: [
                    {
                        label: 'Площадь спортивных зон на человека, м^2',
                        backgroundColor: '#ec0e43',
                        data: Object.values(this.hexReport.area_types_coverage).map(square => square / this.hexReport.total_population)
                    }
                ]
            }
        },
        center() {
            if (!this.hexReport) return ;
            console.log(this.coordinates)
            const center = this.getCentroid(this.coordinates)
            console.log(center)
            return center
        },
        coordinates() {
            if (!this.hexReport) return ;
            return this.hexReport.polygon.coordinates[0][0].map(i => [i[1], i[0]])
        }
    },
    methods: {
        getCentroid (arr) {
            return arr.reduce(function (x,y) {
                return [x[0] + y[0]/arr.length, x[1] + y[1]/arr.length]
            }, [0,0])
        }
    },
    mounted(){
        this.$store.dispatch("getHexReport", {isBig: this.$route.params.isBig, ids: {ids: JSON.parse(this.$route.params.ids)}})
    },
}
</script>
<style>
</style>