class LessonRepository {
  async getLessons(req) {
    throw new Error("Method getLessons() must be implemented.");
  }
  async createLesson(req, data) {
    throw new Error("Method createLesson() must be implemented.");
  }
}

module.exports = LessonRepository;
