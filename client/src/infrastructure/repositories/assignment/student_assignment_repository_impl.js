const StudentAssignmentRepository = require("../../../domain/repositories/assignment/student_assignment_repository");

const assignmentStudentApi = require("../../api/assignment/assignment_student_api");

class StudentAssignmentRepositoryImpl extends StudentAssignmentRepository {
  async getStudentAssignment(req, params) {
    const response = await assignmentStudentApi.getStudentAssignment(
      req,
      params,
    );

    if (!response || response.success !== true) {
      throw new Error(response?.message || "Không thể tải bài tập.");
    }

    return response.data;
  }

  async saveAnswers(req, data) {
    const response = await assignmentStudentApi.saveAnswers(req, data);

    if (!response || response.success !== true) {
      throw new Error(response?.message || "Không thể lưu bài làm.");
    }

    return response.data;
  }

  async submitAssignment(req, data) {
    const response = await assignmentStudentApi.submitAssignment(req, data);

    if (!response || response.success !== true) {
      throw new Error(response?.message || "Không thể nộp bài.");
    }

    return response.data;
  }
}

module.exports = StudentAssignmentRepositoryImpl;
