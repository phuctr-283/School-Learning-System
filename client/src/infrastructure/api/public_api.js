const axios = require("axios");
const publicApi = axios.create({
    baseURL: process.env.DJANGO_API_URL,
    headers: {
    "Content-Type": "application/json",
  },
});
module.exports = publicApi;