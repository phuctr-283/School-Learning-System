class AssignmentRepository {
  async createAssignment(req, assignmentDTO) {
    throw new Error(
      "createAssignment() chưa được triển khai.",
    );
  }

  async getAssignments(req, params = {}) {
    throw new Error(
      "getAssignments() chưa được triển khai.",
    );
  }
  async getAssignmentsBySubject(req, subjectId) {
    throw new Error(
      "getAssignmentsBySubject() chưa được triển khai.",
    );
  }
  async getAssignmentById(req, assignmentId) {
    throw new Error(
      "getAssignmentById() chưa được triển khai.",
    );
  }
}

module.exports = AssignmentRepository;