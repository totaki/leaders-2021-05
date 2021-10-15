import Vue from "vue";
import Vuex from 'vuex'
import api from "./api"

Vue.use(Vuex)

const state = {
  departments: []
}

const getters = {
  departments: state => state.departments
}

const actions = {
  getDepartments: ({ commit }) => {
    api.getDepartments()
      .then(r => {
        commit("SET_DEPARTMENTS", r.data)
      })
  }
}

const mutations = {
  SET_DEPARTMENTS: (state, departments) => {state.departments = departments}
}

export default new Vuex.Store({
    state,
    getters,
    actions,
    mutations
})