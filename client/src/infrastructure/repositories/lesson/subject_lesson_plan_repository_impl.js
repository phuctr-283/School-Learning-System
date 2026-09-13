const SubjectLessonPlanRepository = require("../../../domain/repositories/lesson/subject_lesson_plan_repository");

const lessonApi = require("../../api/lesson/lesson_api");

const SubjectLessonPlanDTO = require("../../../application/lessons/dto/subject_lesson_plan.dto");

class SubjectLessonPlanRepositoryImpl extends SubjectLessonPlanRepository {
  // =========================================
  // GET SUBJECT LESSON PLANS
  // =========================================

  async getSubjectLessonPlans(req) {
    try {
      const response = await lessonApi.getSubjectLessonPlans(req);

      if (!response.success) {
        throw new Error(
          response.message || "Không thể lấy kế hoạch buổi học môn học",
        );
      }

      const plans = response.data || [];

      return plans.map((item) => new SubjectLessonPlanDTO(item));
    } catch (error) {
      console.error(
        "GET SUBJECT LESSON PLANS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy kế hoạch buổi học môn học",
      );
    }
  }
  // =========================================
  // CREATE
  // =========================================

  async createSubjectLessonPlan(req, data) {
    try {
      const response = await lessonApi.createSubjectLessonPlan(
        req,
        data.toJSON(),
      );

      if (!response.success) {
        throw new Error(
          response.message || "Không thể tạo quy tắc kế hoạch môn học",
        );
      }

      const plans = response.data || [];

      return plans.map((item) => new SubjectLessonPlanDTO(item));
    } catch (error) {
      console.error(
        "CREATE SUBJECT LESSON PLANS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể tạo quy tắc kế hoạch môn học",
      );
    }
  }
}

module.exports = SubjectLessonPlanRepositoryImpl;
