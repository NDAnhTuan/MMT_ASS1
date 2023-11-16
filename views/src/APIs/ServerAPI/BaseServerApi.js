import axios from "axios";

const BaseServerApi = axios.create({
  //baseURL: "http://192.168.1.9:5000",
   baseURL: "http://localhost:5050",
  headers: {
    "Content-Type": "application/json",
  },
});

export const baseURL = "http://localhost:5050";

export default BaseServerApi;
