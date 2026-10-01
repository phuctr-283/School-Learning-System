const AssignmentApplicationRepository = require("../../../domain/repositories/assignment/assignment_application_repository");

const AssignmentApplicationDTO = require("../../../application/assignments/dto/assignment_application.dto");
const AssignmentApplicationContentDTO = require("../../../application/assignments/dto/assignment_application_content.dto");
const assignmentApi = require("../../api/assignment/assignment_api");
const errorApi = require("../../api/error_api");

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
  async verifyStudentAssignmentQr(payload) {
    try {
      const response = await assignmentApi.verifyStudentAssignmentQr(payload);

      if (!response || response.success !== true) {
        throw new errorApi(
          response?.message || "Không thể xác thực bài tập.",
          400,
          response,
        );
      }

      return response.data;
    } catch (error) {
      console.log("========== QR API ERROR ==========");

      console.log("STATUS:", error.response?.status);

      console.log("DATA:", error.response?.data);

      console.log("MESSAGE:", error.message);

      console.log("==================================");

      throw new errorApi(
        error.response?.data?.message ||
          error.message ||
          "Không thể xác thực bài tập.",
        error.response?.status || 500,
        error.response?.data || null,
      );
    }
  }
  async getStudentAssignmentApplications(req, classSectionId, lessonId) {
    const response = await assignmentApi.getStudentAssignmentApplications(
      req,
      classSectionId,
      lessonId,
    );

    const data = response?.data ?? [];

    return data.map((item) => new AssignmentApplicationContentDTO(item));
  }
  async getStudentAssignmentAttempts(
    req,
    { assignmentApplicationId, classSectionId, lessonId },
  ) {
    try {
      const response = await assignmentApi.getStudentAssignmentAttempts(req, {
        assignmentApplicationId,
        classSectionId,
        lessonId,
      });

      if (!response || response.success !== true) {
        throw new Error(
          response?.message || "Không thể lấy danh sách sinh viên.",
        );
      }

      return response.data;
    } catch (error) {
      const backendData = error.response?.data;

      console.error(
        "GET STUDENT ASSIGNMENT ATTEMPTS ERROR:",
        backendData || error.message,
      );

      if (backendData?.message) {
        throw new Error(backendData.message);
      }

      throw new Error(error.message || "Không thể lấy danh sách sinh viên.");
    }
  }
}

module.exports = AssignmentApplicationRepositoryImpl;
