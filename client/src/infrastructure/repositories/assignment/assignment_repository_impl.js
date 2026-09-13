const AssignmentRepository = require("../../../domain/repositories/assignment/assignment_repository");

const assignmentApi = require("../../api/assignment/assignment_api");

const AssignmentDTO = require("../../../application/assignments/dto/assignment.dto");

const AssignmentContentDTO = require("../../../application/assignments/dto/assignment_content.dto");
class AssignmentRepositoryImpl extends AssignmentRepository {
  async createAssignment(createAssignmentDTO) {
    try {
      const response = await assignmentApi.createAssignment(
        createAssignmentDTO.toRequestBody(),
      );

      return response.data;
    } catch (error) {
      throw this.normalizeError(error, "Không thể tạo bài tập");
    }
  }

  async getAssignments() {
    try {
      const response = await assignmentApi.getAssignments();

      const items = Array.isArray(response.data) ? response.data : [];

      return items.map((item) => new AssignmentDTO(item));
    } catch (error) {
      throw this.normalizeError(error, "Không thể tải danh sách bài tập");
    }
  }
}

module.exports = AssignmentRepositoryImpl;
