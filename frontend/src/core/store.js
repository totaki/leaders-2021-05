import Vue from "vue";
import Vuex from 'vuex'
import api from "./api"
import axios from "axios";

Vue.use(Vuex)

const state = {
  departments: [],
  facilities: [],
  areaTypes: [],
  sportTypes: [],
  selectedFacility: null,
  facilityFilter: {department: null},
  facilitiesCancelTokenSource: axios.CancelToken.source()
}

const getters = {
  departments: state => state.departments,
  facilities: state => state.facilities,
  areaTypes: state => state.areaTypes,
  sportTypes: state => state.sportTypes,
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
  getAreaTypes: ({commit}) => {
    api.getAreaTypes()
      .then(r => {
        commit("SET_AREA_TYPES", r.data)
      })
  },
  getSportTypes: ({commit}) => {
    api.getSportTypes()
      .then(r => {
        commit("SET_SPORT_TYPES", r.data)
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
    state.facilitiesCancelTokenSource.cancel();
    commit("SET_NEW_FACILITY_CANCEL_TOKEN")
    let requests = tiles.map(([x, y, zoom]) => api.getFacilities({
      tile: `${zoom}/${x}/${y}`,
      availability: [3, 4],
      limit: 150, ...facilityFilter
    }, state.facilitiesCancelTokenSource.token))
    requests.push(
      api.getFacilities({availability: [1, 2], limit: 600, ...facilityFilter}, state.facilitiesCancelTokenSource.token),
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
  SET_AREA_TYPES: (state, items) => {
    state.areaTypes = items
  },
  SET_SPORT_TYPES: (state, items) => {
    state.sportTypes = items
  },
  SET_SELECTED_FACILITY: (state, item) => {
    state.selectedFacility = item
  },
  SET_FACILITY_FILTER: (state, item) => {
    state.facilityFilter = item
  },
  SET_NEW_FACILITY_CANCEL_TOKEN: (state) => {
    state.facilitiesCancelTokenSource = axios.CancelToken.source()
  },
}

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})