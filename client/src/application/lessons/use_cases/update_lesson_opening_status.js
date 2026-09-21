class UpdateLessonOpeningStatusUseCase {
  constructor(lessonOpeningRepository) {
    this.lessonOpeningRepository = lessonOpeningRepository;
  }

  async execute(req, { classSectionLessonPlanId, lessonId, status }) {
    if (!classSectionLessonPlanId) {
      throw new Error("Class section lesson plan ID không được để trống.");
    }

    if (!lessonId) {
      throw new Error("Lesson ID không được để trống.");
    }

    const allowedStatuses = ["locked", "open", "closed"];

    if (!allowedStatuses.includes(status)) {
      throw new Error("Trạng thái buổi học không hợp lệ.");
    }

    return this.lessonOpeningRepository.updateStatus(
      req,
      classSectionLessonPlanId,
      lessonId,
      status,
    );
  }
}

module.exports = UpdateLessonOpeningStatusUseCase;
