class CreateLessonUseCase {
  constructor(lessonRepository) {
    this.lessonRepository = lessonRepository;
  }

  async execute(req, data) {
    return await this.lessonRepository.createLesson(req, data);
  }
}

module.exports = CreateLessonUseCase;
