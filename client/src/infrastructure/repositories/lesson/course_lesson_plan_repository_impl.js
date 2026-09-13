const CourseLessonPlanRepository = require("../../../domain/repositories/lesson/course_lesson_plan_repository");

const lessonApi = require("../../api/lesson/lesson_api");

const CourseLessonPlanDTO = require("../../../application/lessons/dto/course_lesson_plan.dto");

class CourseLessonPlanRepositoryImpl extends CourseLessonPlanRepository {
  async getCourseLessonPlans(req) {
    try {
      const response = await lessonApi.getCourseLessonPlans(req);

      if (!response?.success) {
        throw new Error(
          response?.message || "Không thể lấy kế hoạch môn học phần.",
        );
      }

      const plans = response.data || [];

      return plans.map((item) => new CourseLessonPlanDTO(item));
    } catch (error) {
      console.error(
        "GET COURSE LESSON PLANS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy kế hoạch môn học phần.",
      );
    }
  }
}

module.exports = CourseLessonPlanRepositoryImpl;
