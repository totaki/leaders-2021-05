import axios from "axios"

const api = axios.create({
  baseURL: process.env.NODE_ENV === "production" ? "/api/v1" : 'http://localhost:8000/api/v1' ,
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

export default {
  getDepartments,
  getFacilities,
  getFacilitiesByTile,
  getAreaTypes,
  getSportTypes,
}