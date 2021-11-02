import Vue from "vue";
import Vuex from 'vuex'
import api from "./api"
import axios from "axios";

Vue.use(Vuex)

const state = {
  departments: [],
  facilities: [],
  big_hexes: [],
  small_hexes: [],
  areaTypes: [{id:0,name:''}],
  sportTypes: [{id:0,name:''}],
  availabilities: [
    {id: 4, name: "Шаговая доступность"},
    {id: 3, name: "Районная доступность"},
    {id: 2, name: "Окружная доступность"},
    {id: 1, name: "Городского значения"},
  ],
  selectedFacility: null,
  selectedFacilityLayer: false,
  facilityFilter: {department: null},
  facilityReport: {
    name: "",
    availability: 1,
    areas: [
      {
        id: 0,
        name: "",
        sports: [
          0
        ],
        square: 0,
        facility: 0,
        type: 0
      },
    ],
    department: {
      id: 0,
      name: ""
    }
  },
  facilitiesCancelTokenSource: axios.CancelToken.source(),
  lastTilesList: new Set(),
  lastFacilityFilter: null,
  newFacilities: [],
  lastDensityTiles: [],
  selectedHexes: [],
  hexReport: null
}

const getters = {
  departments: state => state.departments,
  facilities: state => state.facilities,
  big_hexes: state => state.big_hexes,
  small_hexes: state => state.small_hexes,
  areaTypes: state => state.areaTypes,
  sportTypes: state => state.sportTypes,
  availabilities: state => state.availabilities,
  selectedFacility: state => state.selectedFacility,
  facilityFilter: state => state.facilityFilter,
  facilityReport: state => state.facilityReport,
  newFacilities: state => state.newFacilities,
  selectedHexes: state => state.selectedHexes,
  hexReport: state => state.hexReport,
  selectedFacilityLayer: state => state.selectedFacilityLayer
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
  getFacilityReport: ({commit}, { id }) => {
    api.getFacilityReport(id)
      .then(r => {
        commit("SET_FACILITY_REPORT", r.data)
      })
  },
  getFacilities: ({commit}, {facilityFilter}) => {
    api.getFacilities(facilityFilter)
      .then(r => {
        commit("SET_FACILITIES", r.data.results)
      })
  },
  getSelectedHexes: ({commit}, hex ) => {
    commit("SET_SELECTED_HEXES", hex)
  },
  getUnitingBigHexes: ({dispatch}) => {
    dispatch('getBigHexes',{api: api.getUnitingBigHexes})
  },
  getDensityBigHexes: ({dispatch}) => {
    dispatch('getBigHexes',{api: api.getPopulationBigHexes})
  },
  getSportBigHexes: ({dispatch}) => {
    dispatch('getBigHexes',{api: api.getSportBigHexes})
  },
  getBigHexes: ({ commit }, {api} ) => {
    api()
      .then(r => {
        commit("SET_BIG_HEXES", r.data.results)
      })
  },
  getUnitingSmallHexes: ({dispatch},{tiles}) => {
    dispatch('getSmallHexes',{tiles,api: api.getUnitingSmallHexes})
  },
  getDensitySmallHexes: ({dispatch},{tiles}) => {
    dispatch('getSmallHexes',{tiles,api: api.getPopulationSmallHexes})
  },
  getSportSmallHexes: ({dispatch},{tiles}) => {
    dispatch('getSmallHexes',{tiles,api: api.getSportSmallHexes})
  },
  getSportIntersectionSmallHexes: ({dispatch},{tiles}) => {
    dispatch('getSmallHexes',{tiles,api: api.getSportIntersectionSmallHexes})
  },
  getSmallHexes: ({commit},{ tiles, api}) => {
    if (JSON.stringify(state.lastDensityTiles) === JSON.stringify(tiles)) return;
    commit("SET_LAST_DENSITY_TILES", tiles)
    const requests = tiles.map(([x, y, zoom]) => api(zoom, x, y))
    let hexes = []
    axios.all(requests).then(axios.spread((...responses) => {
      for (const response of responses) {
        hexes.push(...response.data.results)
      }
      commit("SET_SMALL_HEXES", hexes.filter((item, idx) => hexes.findIndex(hex => hex.id === item.id) === idx))
    })).catch(errors => {
      console.log(errors)
    })
  },
  getSelectedFacility: ({commit}, {facility}) => {
    commit("SET_SELECTED_FACILITY", facility)
  },
  clearNewFacilitiesBuffer: ({commit}) => {
    commit("CLEAR_NEW_FACILITIES_BUFFER")
  },
  getFacilitiesByTiles: async ({commit}, {tiles, facilityFilter}) => {
    const newTiles = tiles.filter(item => !state.lastTilesList.has(JSON.stringify(item)))
    if (!newTiles.length) {
      return;
    }
    commit("UPDATE_LAST_TILES", newTiles)

    state.facilitiesCancelTokenSource.cancel();
    commit("SET_NEW_FACILITY_CANCEL_TOKEN")
    let requests = newTiles.map(([x, y, zoom]) => api.getFacilities({
      tile: `${zoom}/${x}/${y}`,
      availability: [3, 4],
      limit: 150, ...facilityFilter
    }, state.facilitiesCancelTokenSource.token))
    let facilities = []
    axios.all(requests).then(axios.spread((...responses) => {
      for (const response of responses) {
        facilities.push(...response.data.results)
      }
      commit("SET_NEW_FACILITIES", facilities)
    })).catch(errors => {
      console.log(errors)
    })
  },
  getHexReport({commit},{isBig,ids}){
    if (isBig === 'true'){
      console.log("serch big")
      api.getHexBigReport(ids).then( r => {
        commit("SET_HEX_REPORT",r.data)
      })
    } else {
      console.log("serch small")
      api.getHexSmallReport(ids).then( r => {
        commit("SET_HEX_REPORT",r.data)
      })
    }
  }
}

const mutations = {
  SET_DEPARTMENTS: (state, items) => {state.departments = items},
  SET_FACILITIES: (state, items) => {state.facilities = items},
  SET_BIG_HEXES: (state, items) => {
    state.big_hexes = items
  },
  CLEAR_BIG_HEXES: (state) => {
    state.big_hexes = []
  },
  SET_SMALL_HEXES: (state, items) => {
    state.small_hexes = items
  },
  CLEAR_SMALL_HEXES: (state) => {
    state.small_hexes = []
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
  SET_FACILITY_REPORT: (state, item) => {
    state.facilityReport = item
  },
  SET_NEW_FACILITY_CANCEL_TOKEN: (state) => {
    state.facilitiesCancelTokenSource = axios.CancelToken.source()
  },
  UPDATE_LAST_TILES: (state, tiles) => {
    let newList = new Set(state.lastTilesList)
    tiles.forEach(el => newList.add(JSON.stringify(el)))
    state.lastTilesList = newList
  },
  CLEAR_NEW_FACILITIES_BUFFER: (state) => {
    state.newFacilities = []
  },
  CLEAR_TILE_LIST: (state) => {
    state.lastTilesList = new Set();
  },
  SET_NEW_FACILITIES: (state, items) => {
    state.newFacilities = items.map(item => Object.freeze(item))
  },
  SET_LAST_DENSITY_TILES: (state, items) => {
    state.lastDensityTiles = items
  },
  CLEAR_LAST_DENSITY_TILES: (state) => {
    state.lastDensityTiles = []
  },
  SET_SELECTED_HEXES: (state, item) => {
    if (state.selectedHexes.find( hex=>hex === item)) {
      state.selectedHexes.splice(state.selectedHexes.findIndex(hex => hex === item),1)
      return
    }
    state.selectedHexes.push(item)
  },
  CLEAR_SELECTED_HEXES: (state) => {
    state.selectedHexes = []
  },
  SET_HEX_REPORT: (state, item) => {
    state.hexReport = item
  },
  SET_SELECTED_FACILITY_LAYER: (state, item) => {
    state.selectedFacilityLayer = item
  }
}

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})