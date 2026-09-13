const authenticatedApi = require("../authenticated_api");

const subjectApi = {
  async getUniversitySubjects(req, config = {}) {
    const response = await authenticatedApi.get(req, "/subjects/list/", config);

    return response.data;
  },
  async createSubject(req, data, config = {}) {
    const response = await authenticatedApi.post(
      req,
      "/subjects/create/",
      data,
      config,
    );

    return response.data;
  },
};

module.exports = subjectApi;
