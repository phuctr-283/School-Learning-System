const SemesterLessonPlanRepository = require("../../../domain/repositories/lesson/semester_lesson_plan_repository");

const lessonApi = require("../../api/lesson/lesson_api");

const SemesterLessonPlanDTO = require("../../../application/lessons/dto/semester_lesson_plan.dto");

class SemesterLessonPlanRepositoryImpl extends SemesterLessonPlanRepository {
  // =========================================
  // GET SEMESTER LESSON PLANS
  // =========================================

  async getSemesterLessonPlans(req) {
    try {
      const response = await lessonApi.getSemesterLessonPlans(req);

      if (!response.success) {
        throw new Error(
          response.message || "Không thể lấy kế hoạch buổi học học kỳ",
        );
      }

      const plans = response.data || [];

      return plans.map((item) => new SemesterLessonPlanDTO(item));
    } catch (error) {
      console.error(
        "GET SEMESTER LESSON PLANS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy kế hoạch buổi học học kỳ",
      );
    }
  }
  async createSemesterLessonPlans(req, data) {
    try {
      const response = await lessonApi.createSemesterLessonPlans(
        req,
        data.toJSON(),
      );

      if (!response.success) {
        throw new Error(response.message || "Không thể tạo kế hoạch học kỳ");
      }

      return (response.data || []).map(
        (item) => new SemesterLessonPlanDTO(item),
      );
    } catch (error) {
      console.error(
        "CREATE SEMESTER LESSON PLANS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể tạo kế hoạch học kỳ",
      );
    }
  }
}

module.exports = SemesterLessonPlanRepositoryImpl;
