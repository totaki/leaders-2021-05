import Vue from "vue";
import Vuex from 'vuex'
import api from "./api"

Vue.use(Vuex)

const state = {
  departments: [],
  facilities: []
}

const getters = {
  departments: state => state.departments,
  facilities: state => state.facilities
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
  }

}

const mutations = {
  SET_DEPARTMENTS: (state, items) => {state.departments = items},
  SET_FACILITIES: (state, items) => {state.facilities = items}
}

export default new Vuex.Store({
    state,
    getters,
    actions,
    mutations
})