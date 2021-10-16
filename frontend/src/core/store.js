import Vue from "vue";
import Vuex from 'vuex'
import api from "./api"

Vue.use(Vuex)

const state = {
  departments: [],
  facilities: [],
  selectedFacility: null,
}

const getters = {
  departments: state => state.departments,
  facilities: state => state.facilities,
  selectedFacility: state => state.selectedFacility,
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
  getSelectedFacility: ({ commit }, { facility }) => {commit("SET_SELECTED_FACILITY", facility)},
}

const mutations = {
  SET_DEPARTMENTS: (state, items) => {state.departments = items},
  SET_FACILITIES: (state, items) => {state.facilities = items},
  SET_SELECTED_FACILITY: (state, item) => {state.selectedFacility = item},
}

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})