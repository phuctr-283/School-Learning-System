class GetAssignmentApplicationsUseCase {
  constructor(assignmentApplicationRepository) {
    this.assignmentApplicationRepository = assignmentApplicationRepository;
  }

  async execute(req, { classSectionId, lessonId }) {
    if (!classSectionId) {
      throw new Error("Thiếu mã lớp học phần.");
    }

    if (!lessonId) {
      throw new Error("Thiếu mã lesson.");
    }

    return await this.assignmentApplicationRepository.getByClassSectionAndLesson(
      req,
      classSectionId,
      lessonId,
    );
  }
}

module.exports = GetAssignmentApplicationsUseCase;
