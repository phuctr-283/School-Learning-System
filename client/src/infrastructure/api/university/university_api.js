const publicApi = require("../public_api");
const authenticatedApi = require("../authenticated_api");

const universityApi = {
  async create(req, data, config = {}) {
    const response = await authenticatedApi.post(req,"/universities/create/",data,config,);
    return response.data;
  },

  async getAll(req, config = {}) {
    const response = await authenticatedApi.get(req,"/universities/list/",config,);
    return response.data;
  },
  async getActiveUniversities(config = {}) {
    const response = await publicApi.get("/universities/active/", config);
    return response.data;
  },
};

module.exports = universityApi;
