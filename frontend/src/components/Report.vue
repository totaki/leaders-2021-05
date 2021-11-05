<template>
    <v-app>
        <v-sheet
            color="white"
            elevation="1"
            width="800"
            class="mx-auto mt-2 my-auto pa-6"
            v-if="hexReport"
        >
            <v-container class="px-14">
                <div class="text-h4 text-center pb-4">Информация по выбранным полигонам </div>
                <div class="text-subtitle-1">Общая площадь полигонов: {{hexReport.total_square.toFixed(2)}} км<sup>2</sup> </div>
                <div class="text-subtitle-1">Общая площадь спортивных объктов: {{hexReport.total_sport_square.toFixed(2)}} м<sup>2</sup> </div>
                <div class="text-subtitle-1">Площадь спортивных объектов по типам:</div>
                <ul class="text-body-2 ml-4" v-for="area in Object.entries(hexReport.area_types_coverage)" :key="area[0]">
                    <li>{{areaTypes.find( ar => ar.id === +area[0]).name}}: {{Math.round(area[1])}} м<sup>2</sup></li>
                </ul>
                <div class="text-subtitle-1">Количество спортивных зон:</div>
                <ul class="text-body-2 ml-4" v-for="area in Object.entries(hexReport.area_types_counter)" :key="Math.random(area[0])">
                    <li>{{areaTypes.find( ar => ar.id === +area[0]).name}}: {{Math.round(area[1])}} шт.</li>
                </ul>
                <div class="text-subtitle-1">Количество видов спорта:</div>
                <ul class="text-body-2 ml-4" v-for="(area) in Object.entries(hexReport.sports_counts)" :key="Math.random(area[0])">
                    <li>{{sportTypes.find( ar => ar.id === +area[0]).name}}: {{Math.round(area[1])}} шт.</li>
                </ul>
            </v-container>
        </v-sheet>
    </v-app>

</template>
<script>
export default {
    computed: {
        hexReport(){
            return this.$store.getters.hexReport
        },
        areaTypes() {
            return this.$store.getters.areaTypes;
        },
        sportTypes() {
            return this.$store.getters.sportTypes;
        },
    },
    mounted(){
        this.$store.dispatch("getHexReport", {isBig: this.$route.params.isBig, ids: {ids: JSON.parse(this.$route.params.ids)}})
        
    },
}
</script>
<style>
</style>