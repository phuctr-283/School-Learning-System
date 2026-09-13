class ClassSectionLessonPlanRepository {
  async getClassSectionLessonPlans(req, courseLessonPlanId,) {
    throw new Error(
      "Method getClassSectionLessonPlans() must be implemented.",
    );
  }
  async ensure(req, config = {}) {
    throw new Error(
      "ensure() chưa được triển khai.",
    );
  }
}

module.exports = ClassSectionLessonPlanRepository;