const AssignmentApplicationRepository = require("../../../domain/repositories/assignment/assignment_application_repository");

const assignmentApi = require("../../api/assignment/assignment_api");

const AssignmentApplicationDTO = require("../../../application/assignments/dto/assignment_application.dto");

class AssignmentApplicationRepositoryImpl extends AssignmentApplicationRepository {
  async applyAssignment(req, dto) {
    const response = await assignmentApi.applyAssignment(
      req,
      dto.toRequestBody(),
    );
    if (!response || response.success !== true) {
      throw new Error(response?.message || "Không thể áp dụng bài tập.");
    }
    if (!response.data) {
      throw new Error("API không trả về dữ liệu application.");
    }
    return new AssignmentApplicationDTO(response.data);
  }
  async getByClassSectionAndLesson(req, classSectionId, lessonId) {
    const response = await assignmentApi.getByClassSectionAndLesson(
      req,
      classSectionId,
      lessonId,
    );

    if (!response || response.success !== true) {
      throw new Error(
        response?.message || "Không thể tải bài tập của buổi học.",
      );
    }

    return response.data || [];
  }
  async updateClassSectionStatus(
    req,
    assignmentApplicationId,
    classSectionId,
    status,
  ) {
    const response = await assignmentApi.updateClassSectionStatus(
      req,
      assignmentApplicationId,
      classSectionId,
      status,
    );

    if (!response || response.success !== true) {
      throw new Error(
        response?.message || "Không thể cập nhật trạng thái bài tập.",
      );
    }

    return response.data;
  }
  async verifyStudentAssignmentQr(req, payload) {
    const response =
      await assignmentApi.verifyStudentAssignmentQr(
        req,
        payload,
      );

    if (!response || response.success !== true) {
      throw new Error(response?.message || "Không thể xác thực bài tập.");
    }

    return response.data;
  }
  async getStudentAssignment(req, params) {
    const response = await assignmentApi.getStudentAssignment(
      req,
      params,
    );

    if (!response || response.success !== true) {
      throw new Error(response?.message || "Không thể tải bài tập.");
    }

    return response.data;
  }
}

module.exports = AssignmentApplicationRepositoryImpl;
