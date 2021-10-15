import axios from "axios"

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

const getDepartments = () => api.get("http://127.0.0.1:8000/api/v1/departments?format=json")

export default {
  getDepartments
}