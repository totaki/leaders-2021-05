import axios from "axios"

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

const getDepartments = () => api.get("/departments?format=json")

const getFacilities = (department) => api.get(`/facilities?department=${department}`)

const getBigHexes = () => api.get(`/density/big-hex?limit=3500`)

// const getSmallHexes = (bbox) => api.get(`/density/small-hex?in_bbox=${bbox.join()}&limit=1500`)
const getSmallHexes = (zoom, x, y) => api.get(`/density/small-hex?tile=${zoom}/${x}/${y}&limit=1500`)

export default {
  getDepartments,
  getFacilities,
  getBigHexes,
  getSmallHexes,
}