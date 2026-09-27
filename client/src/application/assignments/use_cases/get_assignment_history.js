class GetAssignmentHistoryUseCase {
  constructor(studentAssignmentRepository) {
    this.studentAssignmentRepository = studentAssignmentRepository;
  }

  async execute(req, assignmentApplicationId, classSectionId, studentId) {
    if (!assignmentApplicationId) {
      throw new Error("Thiếu mã áp dụng bài tập.");
    }

    if (!classSectionId) {
      throw new Error("Thiếu mã lớp học phần.");
    }
    if(!studentId){
        throw new Error("Thiếu mã sinh viên")
    }
    return this.studentAssignmentRepository.getAttemptHistory(
      req,
      assignmentApplicationId,
      classSectionId,
      studentId,
    );
  }
}

module.exports = GetAssignmentHistoryUseCase;
