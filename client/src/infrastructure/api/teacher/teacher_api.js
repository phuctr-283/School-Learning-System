const publicApi = require("../public_api");
const authenticatedApi = require("../authenticated_api");

const teacherApi = {
  async getUniversityTeachers(req, config = {}) {
    const response = await authenticatedApi.get(req, "/teachers/list/", config);

    return response.data;
  },
  async registerTeacher(data, config = {}) {
    const response = await publicApi.post("/teachers/register/", data, config);

    return response.data;
  },
};

module.exports = teacherApi;
