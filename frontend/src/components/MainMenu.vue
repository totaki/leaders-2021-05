<template>
  <div class="menu-wrapper" data-app>
    <v-card
      height="100%"
      width="256"
      class="mx-auto"
    >
      <v-navigation-drawer permanent>
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
                label="Sport type"
                :items="sportTypes"
                item-text="name"
                item-value="id"
                @change="(val) => filter.sport_type = val"
              ></v-autocomplete>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-autocomplete
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
                :items="departments"
                v-on:change="(val) => filter.department = val"
                item-text="name"
                item-value="id"
                label="Select"
                outlined
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
<!--              <v-list-item-content>-->
<!--                    <a href="#" @click="()=> setFacility(item)">{{ item.name }}</a>-->
<!--              </v-list-item-content>-->
            </v-list-item>
          </div>
        </v-list>
      </v-navigation-drawer>
    </v-card>
  </div>
</template>


<script>

export default {
  name: "MainMenu",
  computed: {
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
    }
  },
  data () {
      return {
        right: null,
  
        filter: {},
      }
  },
  methods: {
    setFilters (filter) {
      console.log(filter);
      this.$store.commit("SET_FACILITY_FILTER", {...filter})
    },
    setFacility (facility) {
      this.$store.dispatch("getSelectedFacility", { facility })
    }
  }
}
</script>

<style scoped>
  .menu-wrapper {
    position: fixed;
    right: 16px;
    top: 16px;
    bottom: 16px;
    z-index: 1000;
  }
</style>