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
              <v-autocomplete
                :items="departments"
                v-on:change="setDepartment"
                item-text="name"
                item-value="id"
                label="Select"
                outlined
              ></v-autocomplete>
            </v-list-item-content>
          </v-list-item>
          <div v-for="item in facilities" :key="item.id">
            <v-list-item>
              <v-list-item-content>
                    <a href="#">{{ item.name }}</a>
              </v-list-item-content>
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
    facilities() {
      console.log(this.$store.getters.facilities)
      return this.$store.getters.facilities;
    }
  },
  data () {
      return {
        right: null,
      }
  },
  methods: {
    setDepartment (department) {
      this.$store.dispatch("getFacilities", { department })
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