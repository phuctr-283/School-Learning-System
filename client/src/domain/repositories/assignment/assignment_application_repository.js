class AssignmentApplicationRepository {
  async applyAssignment(req, dto) {
    throw new Error("applyAssignment() chưa được triển khai.");
  }

  async getByClassSectionAndLesson(req, classSectionId, lessonId) {
    throw new Error("getByClassSectionAndLesson() chưa được triển khai.");
  }

  async updateClassSectionStatus(
    req,
    assignmentApplicationId,
    classSectionId,
    status,
  ) {
    throw new Error("updateClassSectionStatus() chưa được triển khai.");
  }
  async verifyStudentAssignmentQr(req,payload){
    throw new Error("verifyStudentAssignmentQr() chưa được triển khai")
  }
  async getStudentAssignment(
    req,
    params,
  ) {
    throw new Error(
      "getStudentAssignment() chưa được triển khai.",
    );
  }
}

module.exports = AssignmentApplicationRepository;
