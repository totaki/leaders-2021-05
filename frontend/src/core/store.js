import Vue from "vue";
import Vuex from 'vuex'
import api from "./api"
import axios from "axios";

Vue.use(Vuex)

const state = {
  departments: [],
  facilities: [],
  big_hexes: [],
  hexes: [],
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
  selectedBaseLayer: null,
  facilityFilter: null,
  sportFilter: null,
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
  hexReport: null,
  hexBins: [],
  layerNames: ["Спортивные объекты","Плотность населения","Плотность спортивных объектов","Объединение населения и объектов"],

}

const getters = {
  departments: state => state.departments,
  facilities: state => state.facilities,
  hexes: state => state.hexes,
  areaTypes: state => state.areaTypes,
  sportTypes: state => state.sportTypes,
  availabilities: state => state.availabilities,
  selectedFacility: state => state.selectedFacility,
  facilityFilter: state => state.facilityFilter,
  sportFilter: state => state.sportFilter,
  facilityReport: state => state.facilityReport,
  newFacilities: state => state.newFacilities,
  selectedHexes: state => state.selectedHexes,
  hexReport: state => state.hexReport,
  selectedBaseLayer: state => state.selectedBaseLayer,
  hexBins: state => state.hexBins,
  layerNames: state => state.layerNames
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
  getUnitingBigHexes: ({dispatch},{tiles}) => {
    dispatch('getHexes',{tiles,api: api.getUnitingBigHexes,filter: state.sportFilter})
  },
  getDensityBigHexes: ({dispatch},{tiles}) => {
    dispatch('getHexes',{tiles,api: api.getPopulationBigHexes})
  },
  getSportBigHexes: ({dispatch},{tiles}) => {
    dispatch('getHexes',{tiles,api: api.getSportBigHexes,filter: state.sportFilter})
  },
  getUnitingSmallHexes: ({dispatch},{tiles}) => {
    dispatch('getHexes',{tiles,api: api.getUnitingSmallHexes,filter: state.sportFilter})
  },
  getDensitySmallHexes: ({dispatch},{tiles}) => {
    dispatch('getHexes',{tiles,api: api.getPopulationSmallHexes})
  },
  getSportSmallHexes: ({dispatch},{tiles}) => {
    dispatch('getHexes',{tiles,api: api.getSportSmallHexes,filter: state.sportFilter})
  },
  getSportIntersectionSmallHexes: ({dispatch},{tiles}) => {
    dispatch('getHexes',{tiles,api: api.getSportIntersectionSmallHexes})
  },
  getHexes: ({commit},{ tiles, api, filter}) => {
    if (JSON.stringify(state.lastDensityTiles) === JSON.stringify(tiles)) return;
    commit("SET_LAST_DENSITY_TILES", tiles)
    const requests = tiles.map(([x, y, zoom]) => api(zoom, x, y, filter))
    let hexes = []
    axios.all(requests).then(axios.spread((...responses) => {
      for (const response of responses) {
        hexes.push(...response.data.results)
      }
      commit("SET_HEXES", hexes.filter((item, idx) => hexes.findIndex(hex => hex.id === item.id) === idx))
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
  getHexReport({commit},{isBig,ids}) {
    if (isBig === 'true') {
      api.getHexBigReport(ids).then(r => {
        commit("SET_HEX_REPORT", r.data)
      })
    } else {
      api.getHexSmallReport(ids).then(r => {
        commit("SET_HEX_REPORT", r.data)
      })
    }
  },
  getHexBins({commit},params){
    switch (state.selectedBaseLayer) {
      case state.layerNames[1]:
        if (params.is_big_hexes) {
          console.log("GETTING BINS BIG POPULATION")
          commit("SET_HEX_BINS", [27, 379, 1900, 6627, 11525, 17106, 23040, 26530, 43127])
          break;
        }
        console.log("GETTING BINS SMALL POPULATION")
        commit("SET_HEX_BINS", [5, 22, 360, 1597, 2661, 3805, 4739, 5333, 11000])
        break;
      case state.layerNames[2]:
        api.getColorBinsBySquare(params)
            .then(r => {
              console.log("GETTING BINS",r.data[0].bins)
              commit("SET_HEX_BINS",r.data[0].bins)
            })
        break;
      case state.layerNames[3]:
        api.getColorBinsBySquarePerPerson(params)
            .then(r => {
              console.log("GETTING BINS PER PERSON",r.data[0].bins)
              commit("SET_HEX_BINS",r.data[0].bins)
            })
        break;
    }
  }
}

const mutations = {
  SET_DEPARTMENTS: (state, items) => {state.departments = items},
  SET_FACILITIES: (state, items) => {state.facilities = items},
  SET_HEXES: (state, items) => {
    state.hexes = items
  },
  CLEAR_HEXES: (state) => {
    state.hexes = []
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
  SET_SPORT_FILTER: (state, item) => {
    state.sportFilter = item
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
  SET_BASE_LAYER: (state, item) => {
    state.selectedBaseLayer = item
  },
  SET_HEX_BINS: (state,item) => {
    state.hexBins = item
  }
}

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})