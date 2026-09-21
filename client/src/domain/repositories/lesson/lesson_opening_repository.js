class LessonOpeningRepository {
  async getLessonOpenings(req, classSectionLessonPlanId) {
    throw new Error("getLessonOpenings() chưa được triển khai.");
  }
  async updateStatus(req, classSectionLessonPlanId, lessonId, status) {
    throw new Error("Method updateStatus() must be implemented.");
  }
}

module.exports = LessonOpeningRepository;
