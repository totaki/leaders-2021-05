import axios from "axios"

const api = axios.create({
  baseURL: process.env.NODE_ENV === "production" ? "/api/v1" :'http://localhost:8000/api/v1',
});

function serialize(obj) {
  let str = [];
  for (let p in obj)
    if (Object.prototype.hasOwnProperty.call(obj, p)) {
      if (Array.isArray(obj[p])) {
        for (const val of obj[p]) {
          str.push(encodeURIComponent(p) + "=" + encodeURIComponent(val));
        }
      } else if (obj[p] || obj[p] == 0) {
        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
      }
    }
  return str.join("&");
}

const getDepartments = () => api.get("/departments?format=json")

const getFacilities = (params, cancelToken) => {
  return api.get(`/facilities?${serialize(params)}`, {cancelToken})
}

const getFacilitiesByTile = (zoom, x, y) => api.get(`/facilities?tile=${zoom}/${x}/${y}&limit=1500`)

const getAreaTypes = () => api.get(`/sport-area-types`)
const getSportTypes = () => api.get(`/sport-types`)
const getFacilityReport = (id) => api.get(`/facilities/${id}/report`)

const getPopulationBigHexes = () => api.get(`/data-hex/big-hex/population-density?limit=3500`)
const getSportBigHexes = () => api.get(`/data-hex/big-hex/sport-density?limit=4000`)
const getUnitingBigHexes = () => api.get(`/data-hex/big-hex?limit=4000`)

const getUnitingSmallHexes = (zoom, x, y) => api.get(`/data-hex/small-hex?tile=${zoom}/${x}/${y}&limit=1500`)
const getPopulationSmallHexes = (zoom, x, y) => api.get(`/data-hex/small-hex/population-density?tile=${zoom}/${x}/${y}&limit=1500`)
const getSportSmallHexes = (zoom, x, y) => api.get(`/data-hex/small-hex/sport-density?tile=${zoom}/${x}/${y}&limit=1500`)
const getSportIntersectionSmallHexes = (zoom, x, y) => api.get(`/sport-density/small-hex-intersections?tile=${zoom}/${x}/${y}&limit=1500`)

export default {
  getDepartments,
  getFacilities,
  getFacilitiesByTile,
  getAreaTypes,
  getSportTypes,
  getFacilityReport,
  getPopulationBigHexes,
  getSportBigHexes,
  getUnitingBigHexes,
  getUnitingSmallHexes,
  getPopulationSmallHexes,
  getSportSmallHexes,
  getSportIntersectionSmallHexes,
}