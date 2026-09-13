const authenticatedApi = require("../authenticated_api");
const publicApi = require("../public_api");

const schoolAdminApi = {
  async getAll(req, config = {}) {
    const response = await authenticatedApi.get(
      req,
      "/school-admins/list/",
      config,
    );

    return response.data;
  },
  async register(data, config = {}) {
    const response = await publicApi.post(
      "/school-admins/register/",
      data,
      config,
    );

    return response.data;
  },
};

module.exports = schoolAdminApi;
