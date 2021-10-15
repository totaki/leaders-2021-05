import axios from "axios"

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

const getDepartments = () => api.get("/departments?format=json")

const getFacilities = (department) => api.get(`/facilities?department=${department}`)

export default {
  getDepartments,
  getFacilities
}