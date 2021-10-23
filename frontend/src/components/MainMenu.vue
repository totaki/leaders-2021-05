<template>
  <div>
     <v-layout fill-height>
      <v-navigation-drawer v-model="filterDrawer" stateless app>
        <v-list-item>
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

        <v-list
          dense
          nav
        >
          <v-list-item>
            <v-list-item-content>
              <v-text-field
                label="Name sport object"
                @input="(val) => filter.name = val"
              ></v-text-field>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-text-field
                label="Area name"
                @input="(val) => filter.area_name = val"
              ></v-text-field>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-autocomplete
                multiple
                clearable
                label="Sport type"
                :items="sportTypes"
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
                label="Area type"
                :items="areaTypes"
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
                label="Availability"
                :items="availabilities"
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
                item-text="name"
                item-value="id"
                label="Departaments"
              ></v-autocomplete>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-btn @click="() => setFilters(filter)">Apply</v-btn>
            </v-list-item-content>
          </v-list-item>
          <div v-for="item in facilities.slice(0,100)" :key="item.id">
            <v-list-item>
             <v-list-item-content>-->
                   <a href="#" @click="()=> setFacility(item)">{{ item.name }}</a>
              </v-list-item-content>
            </v-list-item>
          </div>
        </v-list>
      </v-navigation-drawer>
      <v-navigation-drawer  hide-overlay stateless  v-model='infoDrawer' app>
        <v-card v-if="facilityReport" elevation="0">
          <v-card-actions >
            <v-list-item @click="closeInfo"><v-icon left>mdi-chevron-left</v-icon> Back</v-list-item>
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
      console.log(this.$store.getters.facilities)
      return this.$store.getters.facilities;
    },
    facilityReport(){
      return this.$store.getters.facilityReport;
    }
  },
  watch: {
    facilityReport(val){
      this.showInfo(val)
    }
  },
  data () {
      return {
        right: null,
  
        filter: {},
        filterDrawer: true,
        infoDrawer: false,
      }
  },
  methods: {
    setFilters (filter) {
      console.log(filter);
      this.$store.commit("SET_FACILITY_FILTER", {...filter})
    },
    setFacility (facility) {
      this.$store.dispatch("getSelectedFacility", { facility })
    },
    showInfo(facility){
      console.log(facility)
      this.infoDrawer = true
      this.filterDrawer = false
    },
    closeInfo(){
      this.filterDrawer = true
      this.infoDrawer = false

    }
  }
}
</script>

<style scoped>

</style>