const publicApi = require("../public_api");

class AssignmentStudentApi {
  async getStudentAssignment(params = {}) {
    const response = await publicApi.get("/assignments/student/take/", {
      params,
    });

    return response.data;
  }

  async saveAnswers(data) {
    const response = await publicApi.post(
      "/assignments/student/take/save/",
      data,
    );

    return response.data;
  }

  async submitAssignment(data) {
    const response = await publicApi.post(
      "/assignments/student/take/submit/",
      data,
    );

    return response.data;
  }
  async getAssignmentHistory(
  req,
  assignmentApplicationId,
  classSectionId,
  studentId,
  config = {}
) {
  const response =
    await authenticatedApi.get(
      req,
      `/assignments/student/assignments/${encodeURIComponent(
        assignmentApplicationId
      )}/history/${encodeURIComponent(
        classSectionId
      )}/student/${encodeURIComponent(
        studentId
      )}/`,
      config
    );

  return response.data;
}
}

module.exports = new AssignmentStudentApi();
