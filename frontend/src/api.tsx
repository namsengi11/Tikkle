import axios from "axios";

const api = axios.create({
  baseURL: "http://tikkle.sjnam.site/api",
});

export default api;
