<template>
  <div>
     <v-layout fill-height>
      <v-navigation-drawer permanent stateless app
      >
        <div v-if="currentMenu===0" >
          <v-list-item >
            <v-list-item-content>
              <v-list-item-title class="text-h6">
                Application
              </v-list-item-title>
              <v-list-item-subtitle>
                subtext
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
          <v-list>
            <v-list-item-group >
              <v-list-item @click="currentMenu = 1">
                <v-list-item-title>Аналитика</v-list-item-title>
              </v-list-item>
              <v-list-item @click="currentMenu = 2">
                <v-list-item-title>Объекты</v-list-item-title>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </div>


        <v-list nav v-if="currentMenu===1">
          <v-list-item-group>
            <v-list-item @click="currentMenu = 0"><v-icon left>mdi-chevron-left</v-icon>Назад</v-list-item>
            <v-divider/>
          </v-list-item-group>
          <div class="text-body-2 mx-4 mt-4">Раздел фильтрации для слоя с плотностью спортивных объектов и слоя с объединением плотностей населениея и спортивных объектов</div>
          <v-list dense nav>
            <v-list-item>
              <v-list-item-content>
                <v-autocomplete
                        clearable
                        label="Вид спорта"
                        :items="sportTypes"
                        :value="sportFilter.sports"
                        item-text="name"
                        item-value="id"
                        @change="(val) => sportFilter.sports = val"
                ></v-autocomplete>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-autocomplete
                        clearable
                        label="Тип спортивной зоны"
                        :items="areaTypes"
                        item-text="name"
                        item-value="id"
                        :value="sportFilter.area_type"
                        @change="(val) => sportFilter.area_type = val"
                ></v-autocomplete>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-autocomplete
                        clearable
                        label="Доступность"
                        :items="availabilities"
                        :value="sportFilter.availability"
                        item-text="name"
                        item-value="id"
                        @change="(val) => sportFilter.availability = val"
                ></v-autocomplete>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-autocomplete
                        clearable
                        :items="departments"
                        :value="sportFilter.department"
                        v-on:change="(val) => sportFilter.department = val"
                        item-text="name"
                        item-value="id"
                        label="Ведомостная пренадлежность"
                ></v-autocomplete>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-btn color="primary" outlined @click="() => setSportFilters(sportFilter)">Применить</v-btn>
              </v-list-item-content>
            </v-list-item>
            <v-list-item v-if="isSportFilterSet">
              <v-list-item-content>
                <v-btn color="error" outlined @click="() => {$store.commit('SET_SPORT_FILTER',null)}">Очистить</v-btn>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-list>


        <v-list nav v-if="currentMenu===2">
          <v-list-item-group >
            <v-list-item @click="currentMenu = 0"><v-icon left>mdi-chevron-left</v-icon>Назад</v-list-item>
            <v-divider/>
              <div class="text-body-2 mx-4 mt-4">Раздел фильтрации спортивных объектов</div>
          </v-list-item-group>
          <v-list dense nav>
            <v-list-item>
              <v-list-item-content>
                <v-text-field
                        label="Название спортивного объекта"
                        :value="filter.name"
                        @input="(val) => filter.name = val"
                ></v-text-field>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-text-field
                        label="Название спортивной зоны"
                        :value="filter.area_name"
                        @input="(val) => filter.area_name = val"
                ></v-text-field>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-autocomplete
                        multiple
                        clearable
                        label="Вид спорта"
                        :items="sportTypes"
                        :value="filter.sports"
                        item-text="name"
                        item-value="id"
                        @change="(val) => filter.sports = val"
                ></v-autocomplete>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-autocomplete
                        clearable
                        label="Тип спортивной зоны"
                        :items="areaTypes"
                        :value="filter.area_type"
                        item-text="name"
                        item-value="id"
                        @change="(val) => filter.area_type = val"
                ></v-autocomplete>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-autocomplete
                        clearable
                        label="Доступность"
                        :items="availabilities"
                        :value="filter.availability"
                        item-text="name"
                        item-value="id"
                        @change="(val) => filter.availability = val"
                ></v-autocomplete>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-autocomplete
                        clearable
                        :items="departments"
                        v-on:change="(val) => filter.department = val"
                        :value="filter.department"
                        item-text="name"
                        item-value="id"
                        label="Ведомостная пренадлежность"
                ></v-autocomplete>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-btn color="primary" outlined @click="() => setFilters(filter)">Применить</v-btn>
              </v-list-item-content>
            </v-list-item>
            <v-list-item v-if="isFacilityFilterSet">
              <v-list-item-content>
                <v-btn color="error" outlined @click="() => {$store.commit('SET_FACILITY_FILTER',null)}">Очистить</v-btn>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-list>

        <v-spacer/>

        <v-list-item v-if="isSportFilterSet && isFacilityFilterSet && currentMenu === 0">
          <v-list-item-content>
            <v-btn color="error" outlined @click="() => {$store.commit('SET_SPORT_FILTER',null); $store.commit('SET_FACILITY_FILTER',null)}">Очистить все фильтры</v-btn>
          </v-list-item-content>
        </v-list-item>
      </v-navigation-drawer>

      <v-navigation-drawer  hide-overlay stateless  v-model='infoDrawer' app>
        <v-card v-if="facilityReport" elevation="0">
          <v-card-actions >
            <v-list-item @click="closeInfo"><v-icon left>mdi-chevron-left</v-icon> Назад</v-list-item>
          </v-card-actions>
          <v-divider/>
          <v-card-title>
            <div >
              {{facilityReport.name}}
            </div>
            <div class="text-caption">
              {{availabilities.find( el => facilityReport.availability === el.id).name}}
            </div>
          </v-card-title>
          <v-card-subtitle>
            <div class="text-subtitle-1">
              {{facilityReport.department.name}}
            </div>
          </v-card-subtitle>
          <v-divider/>
          <v-card-text>
              <v-expansion-panels multiple flat accordion>
                <v-expansion-panel
                  v-for="area in facilityReport.areas"
                  :key="area.id"
                >
                  <v-expansion-panel-header>
                    {{area.name}}
                  </v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <div>
                      <strong>Square:</strong> {{area.square}} km
                    </div>
                    <div >
                      <strong>Area type:</strong> {{areaTypes.find(type => type.id === area.type).name}}
                    </div>
                    <div>
                      <strong>Sports:</strong> {{sportTypes.filter( type => area.sports.find(el => el === type.id)).map(el=> el.name).join(', ')}}
                    </div>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
          </v-card-text>

        </v-card>
        </v-navigation-drawer>
     </v-layout >
  </div>
</template>


<script>

export default {
  name: "MainMenu",
  computed: {
    console: ()=>console,
    departments() {
      return this.$store.getters.departments;
    },
    areaTypes() {
      return this.$store.getters.areaTypes;
    },
    sportTypes() {
      return this.$store.getters.sportTypes;
    },
    availabilities() {
      return this.$store.getters.availabilities;
    },
    facilities() {
      return this.$store.getters.facilities;
    },
    facilityReport(){
      return this.$store.getters.facilityReport;
    },
    isSportFilterSet(){
      return !!this.$store.getters.sportFilter
    },
    isFacilityFilterSet(){
      return !!this.$store.getters.facilityFilter
    },
  },
  watch: {
    facilityReport(val){
      this.showInfo(val)
    },
    showFilter(val) {
      this.filterDrawer = val
    }
  },
  data () {
      return {
        right: null,
        currentMenu: 0,
        filter: {},
        sportFilter:{},
        filterDrawer:false,
        infoDrawer: false,
      }
  },
  methods: {
    setFilters (filter) {
      this.$store.commit("SET_FACILITY_FILTER", {...filter})
    },
    setSportFilters (filter) {
      this.$store.commit("SET_SPORT_FILTER", {...filter})
    },
    setFacility (facility) {
      this.$store.dispatch("getSelectedFacility", { facility })
    },
    showInfo(facility){
      console.log(facility)
      this.infoDrawer = true
    },
    closeInfo(){
      this.infoDrawer = false

    }
  }
}
</script>

<style>

</style>