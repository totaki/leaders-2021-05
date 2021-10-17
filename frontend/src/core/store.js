import Vue from "vue";
import Vuex from 'vuex'
import api from "./api"
import axios from "axios";

Vue.use(Vuex)

const state = {
  departments: [],
  facilities: [],
  selectedFacility: null,
  facilityFilter: {department: null}
}

const getters = {
  departments: state => state.departments,
  facilities: state => state.facilities,
  selectedFacility: state => state.selectedFacility,
  facilityFilter: state => state.facilityFilter,
}

const actions = {
  getDepartments: ({commit}) => {
    api.getDepartments()
      .then(r => {
        commit("SET_DEPARTMENTS", r.data)
      })
  },
  getFacilities: ({commit}, {facilityFilter}) => {
    api.getFacilities(...facilityFilter)
      .then(r => {
        commit("SET_FACILITIES", r.data.results)
      })
  },
  getSelectedFacility: ({commit}, {facility}) => {
    commit("SET_SELECTED_FACILITY", facility)
  },
  getFacilitiesByTiles: async ({commit}, {tiles, facilityFilter}) => {
    let requests = tiles.map(([x, y, zoom]) => api.getFacilities({
      tile: `${zoom}/${x}/${y}`,
      availability: [3, 4],
      limit: 150, ...facilityFilter
    }))
    requests.push(
      api.getFacilities({availability: [1, 2], limit: 600, ...facilityFilter}),
    )
    let facilities = []
    axios.all(requests).then(axios.spread((...responses) => {
      for (const response of responses) {
        facilities.push(...response.data.results)
      }
      commit("SET_FACILITIES", facilities)
    })).catch(errors => {
      console.log(errors)
    })
  }
}

const mutations = {
  SET_DEPARTMENTS: (state, items) => {
    state.departments = items
  },
  SET_FACILITIES: (state, items) => {
    state.facilities = items
  },
  SET_SELECTED_FACILITY: (state, item) => {
    state.selectedFacility = item
  },
  SET_FACILITY_FILTER: (state, item) => {
    state.facilityFilter = item
  },
}

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})