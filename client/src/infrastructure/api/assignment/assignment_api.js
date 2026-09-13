const authenticatedApi = require("../authenticated_api");

const assignmentApi = {
  async create(req, data) {
    const response = await authenticatedApi.post(
      req,
      "/api/assignments/create/",
      data,
    );

    return response.data;
  },

  async getList(req, params = {}) {
    const response = await authenticatedApi.get(
      req,
      "/api/assignments/",
      {
        params,
      },
    );

    return response.data;
  },

  async getById(req, assignmentId) {
    const response = await authenticatedApi.get(
      req,
      `/api/assignments/${assignmentId}/`,
    );

    return response.data;
  },

};

module.exports = assignmentApi;