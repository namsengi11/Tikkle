import axios from "axios";

const api = axios.create({
  baseURL: "http://18.142.49.30/api",
});

export default api;
