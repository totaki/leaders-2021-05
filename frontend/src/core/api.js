import axios from "axios"

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

function serialize(obj) {
  let str = [];
  for (let p in obj)
    if (Object.prototype.hasOwnProperty.call(obj, p)) {
      if (Array.isArray(obj[p])) {
        for (const val of obj[p]) {
          str.push(encodeURIComponent(p) + "=" + encodeURIComponent(val));
        }
      } else if (obj[p]) {
        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
      }
    }
  return str.join("&");
}

const getDepartments = () => api.get("/departments?format=json")

const getFacilities = (params) => {
  return api.get(`/facilities?${serialize(params)}`)
}

const getFacilitiesByTile = (zoom, x, y) => api.get(`/facilities?tile=${zoom}/${x}/${y}&limit=1500`)

export default {
  getDepartments,
  getFacilities,
  getFacilitiesByTile,
}