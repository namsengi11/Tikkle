import axios from "axios";

const api = axios.create({
  baseURL: "http://18.142.49.30/api",
  // baseURL: "http://localhost:8000/api",
});

export default api;
