import Vue from "vue";
import Vuex from 'vuex'
import api from "./api"
import axios from "axios";

Vue.use(Vuex)

const state = {
  departments: [],
  facilities: [],
  big_hexes: localStorage.big_hexes ? JSON.parse(localStorage.big_hexes): [],
  small_hexes: localStorage.initial_small_hexes ? JSON.parse(localStorage.initial_small_hexes): [],
}

const getters = {
  departments: state => state.departments,
  facilities: state => state.facilities,
  big_hexes: state => state.big_hexes,
  small_hexes: state => state.small_hexes
}

const actions = {
  getDepartments: ({ commit }) => {
    api.getDepartments()
      .then(r => {
        commit("SET_DEPARTMENTS", r.data)
      })
  },
  getFacilities: ({ commit }, { department }) => {
    api.getFacilities(department)
      .then(r => {
        commit("SET_FACILITIES", r.data.results)
      })
  },
  getBigHexes: ({ commit }) => {
    api.getBigHexes()
      .then(r => {
        commit("SET_BIG_HEXES", r.data.results)
      })
  },
  getSmallHexes: async ({commit}, {tiles}) => {
    const requests = tiles.map(([x, y, zoom]) => api.getSmallHexes(zoom, x, y))
    let hexes = []
    axios.all(requests).then(axios.spread((...responses) => {
      for (const response of responses) {
        hexes.push(...response.data.results)
      }
      commit("SET_SMALL_HEXES", hexes.filter((item, idx) => hexes.findIndex(hex => hex.id === item.id) === idx))
    })).catch(errors => {
      console.log(errors)
    })
  }
}

const mutations = {
  SET_DEPARTMENTS: (state, items) => {state.departments = items},
  SET_FACILITIES: (state, items) => {state.facilities = items},
  SET_BIG_HEXES: (state, items) => {
    if (!state.big_hexes.length) localStorage.setItem('big_hexes', JSON.stringify(items))
    state.big_hexes = items
  },
  SET_SMALL_HEXES: (state, items) => {
    if (!state.small_hexes.length) localStorage.setItem('initial_small_hexes', JSON.stringify(items))
    state.small_hexes = items
  }
}

export default new Vuex.Store({
    state,
    getters,
    actions,
    mutations
})