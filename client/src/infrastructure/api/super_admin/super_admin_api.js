const authenticatedApi = require("../authenticated_api");
const publicApi = require("../public_api");

const superAdminApi = {
  async register(data, config = {}) {
    const response = await publicApi.post(
      "/super-admins/register/",
      data,
      config,
    );

    return response.data;
  },
};

module.exports = superAdminApi;
