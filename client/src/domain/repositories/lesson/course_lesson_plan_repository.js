class CourseLessonPlanRepository {
  async getCourseLessonPlans(req) {
    throw new Error(
      "Method getCourseLessonPlans() must be implemented.",
    );
  }
  async ensure(req, config = {}) {
    throw new Error(
      "ensure() chưa được triển khai.",
    );
  }
}

module.exports = CourseLessonPlanRepository;