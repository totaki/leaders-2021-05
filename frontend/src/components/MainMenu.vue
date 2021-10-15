<template>
  <div class="menu-wrapper" data-app>
    <v-card
      height="400"
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
              <v-select
                :items="items"
                item-text="name"
                item-value="id"
                label="Select"
                outlined
              ></v-select>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    </v-card>
  </div>
</template>


<script>

export default {
  name: "MainMenu",
  computed: {
    items() {
      return this.$store.getters.departments;
    }
  },
  data () {
      return {
        right: null,
      }
  },
}
</script>

<style scoped>
  .menu-wrapper {
    position: fixed;
    right: 16px;
    top: 16px;
    z-index: 1000;
  }
</style>