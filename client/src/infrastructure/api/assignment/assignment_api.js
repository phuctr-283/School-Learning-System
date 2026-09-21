const authenticatedApi = require("../authenticated_api");
const publicApi = require("../public_api");
const assignmentApi = {
  async createAssignment(req, payload, config = {}) {
    const response = await authenticatedApi.post(
      req,
      "/assignments/create/",
      payload,
      config,
    );

    return response.data;
  },

  async getAssignments(req, params = {}, config = {}) {
    const response = await authenticatedApi.get(req, "/assignments/list/", {
      ...config,
      params,
    });

    return response.data;
  },

  async getAssignmentsBySubject(req, subjectId, config = {}) {
    if (!subjectId) {
      throw new Error("Thiếu mã môn học.");
    }

    const response = await authenticatedApi.get(
      req,
      `/assignments/list/${encodeURIComponent(subjectId)}/`,
      config,
    );

    return response.data;
  },

  async getAssignmentById(req, assignmentId, config = {}) {
    if (!assignmentId) {
      throw new Error("Thiếu mã bài tập.");
    }

    const response = await authenticatedApi.get(
      req,
      `/assignments/${encodeURIComponent(assignmentId)}/`,
      config,
    );

    return response.data;
  },
  async applyAssignment(req, payload, config = {}) {
    const response = await authenticatedApi.post(
      req,
      "/assignments/apply/",
      payload,
      config,
    );
    return response.data;
  },
  async getByClassSectionAndLesson(req, classSectionId, lessonId, config = {}) {
    if (!classSectionId) {
      throw new Error("Thiếu mã lớp học phần.");
    }

    if (!lessonId) {
      throw new Error("Thiếu mã lesson.");
    }

    const response = await authenticatedApi.get(
      req,
      "/assignments/applications/",
      {
        ...config,
        params: {
          class_section_id: classSectionId,
          lesson_id: lessonId,
        },
      },
      
    );
console.log(
    "[NODE] DJANGO ASSIGNMENT APPLICATIONS RESPONSE:",
    response.data,);
    return response.data;
  },
  async updateClassSectionStatus(
    req,
    assignmentApplicationId,
    classSectionId,
    status,
    config = {},
  ) {
    if (!assignmentApplicationId) {
      throw new Error("Thiếu mã application.");
    }

    if (!classSectionId) {
      throw new Error("Thiếu mã lớp học phần.");
    }

    if (!["active", "closed"].includes(status)) {
      throw new Error("Trạng thái phải là active hoặc closed.");
    }

    const response = await authenticatedApi.patch(
      req,
      `/assignments/applications/${encodeURIComponent(
        assignmentApplicationId,
      )}/class-sections/${encodeURIComponent(classSectionId)}/status/`,
      {
        status,
      },
      config,
    );

    return response.data;
  },
  async verifyStudentAssignmentQr(req, payload, config = {}) {
  const response = await publicApi.post(
    "/assignments/student/qr/verify/",
    payload,
    config,
  );

  return response.data;
},
};

module.exports = assignmentApi;
