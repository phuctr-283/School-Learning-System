const authenticatedApi = require("../authenticated_api");

const FormData = require("form-data");
const fs = require("fs");

const classSectionApi = {
  async getUniversityClassSections(req, config = {}) {
    const response = await authenticatedApi.get(
      req,
      "/class-sections/list/",
      config,
    );

    return response.data;
  },
  async importClassSections(req, file) {
    const formData = new FormData();

    formData.append("file", fs.createReadStream(file.path), {
      filename: file.originalname,
      contentType: file.mimetype,
    });

    const response = await authenticatedApi.post(
      req,
      "/class-sections/import/",
      formData,
      {
        headers: formData.getHeaders(),
        maxBodyLength: Infinity,
        maxContentLength: Infinity,
      },
    );

    return response.data;
  },
  async getTeacherSubjects(req, config = {}) {
    const response = await authenticatedApi.get(
      req,
      "/class-sections/teacher/subjects/",
      config,
    );

    return response.data;
  },
  async getTeacherActiveSubjects(req, config = {}) {
    const response = await authenticatedApi.get(
      req,
      "/class-sections/teacher/active-subjects/",
      config,
    );

    return response.data;
  },
  async getTeacherClassSections(req, subjectId, config = {}) {
    const response = await authenticatedApi.get(
      req,
      `/class-sections/teacher/subjects/${subjectId}/class-sections/`,
      config,
    );

    return response.data;
  },
  async importStudents(req, file) {
    const formData = new FormData();
    formData.append("file", fs.createReadStream(file.path), {
      filename: file.originalname,
      contentType: file.mimetype,
    });
    const response = await authenticatedApi.post(
      req,
      "/class-sections/students/import/",
      formData,
      {
        headers: formData.getHeaders(),
        maxBodyLength: Infinity,
        maxContentLength: Infinity,
      },
    );
    return response.data;
  },
  async getStudentClassSections(req, config = {}) {
    const response = await authenticatedApi.get(
      req,
      "/class-sections/student/class-sections/",
      config,
    );

    return response.data;
  },
  async getTeacherActivePlannedSubjects(
    req,
    academicYearId,
    semesterId,
    config = {},
  ) {
    if (!academicYearId) {
      throw new Error("Thiếu mã năm học.");
    }
    if (!semesterId) {
      throw new Error("Thiếu mã học kỳ.");
    }
    const response = await authenticatedApi.get(
      req,
      `/class-sections/teacher/academic-year/${academicYearId}/semester/${semesterId}/subjects`,
      config,
    );

    return response.data;
  },
  async getTeacherActivePlannedClassSections(
    req,
    subjectId,
    academicYearId,
    semesterId,
    config = {},
  ) {
    if (!subjectId) {
      throw new Error("Thiếu mã môn học.");
    }

    if (!academicYearId) {
      throw new Error("Thiếu mã năm học.");
    }

    if (!semesterId) {
      throw new Error("Thiếu mã học kỳ.");
    }

    const response = await authenticatedApi.get(
      req,
      `/class-sections/teacher/academic-year/${academicYearId}/semester/${semesterId}/subjects/${encodeURIComponent(
        subjectId,
      )}/class-sections/`,
      config,
    );
    return response.data;
  },
};

module.exports = classSectionApi;
