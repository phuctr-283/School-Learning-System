const publicApi = require("../public_api");

class AssignmentStudentApi {
  async getStudentAssignment(req,params = {}) {
    const response = await publicApi.get(
      "/assignments/student/take/",
      {
        params,
      },
    );

    return response.data;
  }

  async saveAnswers(req,data) {
    const response = await publicApi.post(
      "/assignments/student/take/save/",
      data,
    );

    return response.data;
  }

  async submitAssignment(req,data) {
    const response = await publicApi.post(
      "/assignments/student/take/submit/",
      data,
    );

    return response.data;
  }
}

module.exports =
  new AssignmentStudentApi();