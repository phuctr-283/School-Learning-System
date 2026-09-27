class GetStudentAssignmentApplicationsUseCase {
  constructor(assignmentApplicationRepository) {
    this.assignmentApplicationRepository = assignmentApplicationRepository;
  }

  async execute({ req, classSectionId, lessonId }) {
    if (!classSectionId) {
      throw new Error("Thiếu mã lớp học phần.");
    }

    if (!lessonId) {
      throw new Error("Thiếu mã bài học.");
    }

    return this.assignmentApplicationRepository.getStudentAssignmentApplications(
      req,
      classSectionId,
      lessonId,
    );
  }
}

module.exports = GetStudentAssignmentApplicationsUseCase;
