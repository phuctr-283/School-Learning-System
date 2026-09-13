const authenticatedApi = require("../authenticated_api");

const semesterApi = {
  // =========================================
  // GET SEMESTERS
  // =========================================

  async getUniversitySemesters(req, config = {}) {
    const response = await authenticatedApi.get(
      req,
      "/semesters/list/",
      config,
    );

    return response.data;
  },
  async getActivePlanned(req, config = {}) {
    const response = await authenticatedApi.get(
      req,
      "/semesters/active-planned/",
      config,
    );

    return response.data;
  },
  async createSemester(req, data, config = {}) {
    const response = await authenticatedApi.post(
      req,
      "/semesters/create/",
      data,
      config,
    );

    return response.data;
  },
};

module.exports = semesterApi;
