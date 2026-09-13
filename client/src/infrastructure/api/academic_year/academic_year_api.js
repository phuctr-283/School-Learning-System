const authenticatedApi = require("../authenticated_api");

const academicYearApi = {
  async getAcademicYears(req, config = {}) {
    const response = await authenticatedApi.get(
      req,
      "/academic-years/list/",
      config,
    );

    return response.data;
  },
  async createAcademicYear(req, data, config = {}) {
    const response = await authenticatedApi.post(
      req,
      "/academic-years/create/",
      data,
      config,
    );

    return response.data;
  },
  async getActiveAndPlannedAcademicYears(req, config = {}) {
    const response = await authenticatedApi.get(
      req,
      "/academic-years/active-planned/",
      config,
    );

    return response.data;
  },
};

module.exports = academicYearApi;
