const publicApi = require("../public_api");

const authApi = {
  async login(data, config = {}) {
    const response = await publicApi.post("/users/login/", data, config);
    return response.data;
  },
  async logout(data, config = {}) {
    const response = await publicApi.post("/users/logout/", data, config);
    return response.data;
  },
  async refreshToken(data, config = {}) {
    const response = await publicApi.post("/users/refresh/", data, config);
    return response.data;
  },
};

module.exports = authApi;
