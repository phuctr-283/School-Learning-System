const publicApi = require("../public_api");
const authenticatedApi = require("../authenticated_api");

const departmentApi = {
  async getUniversityDepartments(req, config = {}) {
    const response = await authenticatedApi.get(
      req,
      "/departments/list/",
      config,
    );

    return response.data;
  },

  async create(req, data, config = {}) {
    const response = await authenticatedApi.post(
      req,
      "/departments/create/",
      data,
      config,
    );
    return response.data;
  },
  async getActiveDepartments(universityId, config = {}) {
    const response = await publicApi.get("/departments/active/", {
      ...config,
      params: {
        university_id: universityId,
      },
    });

    return response.data;
  },
  async getActivesDepartments(
    req,
    config = {},
  ) {

    const response =
      await authenticatedApi.get(
        req,
        "/departments/actives/",
        config,
      );

    return response.data;
  },
};

module.exports = departmentApi;
