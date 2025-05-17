import axios from "axios";

const api = axios.create({
  baseURL: "https://tikkle.sjnam.site/api",
});

export default api;
