class GetLessonOpeningsUseCase {
  constructor(lessonOpeningRepository) {
    this.lessonOpeningRepository = lessonOpeningRepository;
  }

  async execute(req, classSectionId) {
    if (!classSectionId) {
      throw new Error("Thiếu mã lớp học phần.");
    }

    return await this.lessonOpeningRepository.getLessonOpenings(
      req,
      classSectionId,
    );
  }
}

module.exports = GetLessonOpeningsUseCase;
