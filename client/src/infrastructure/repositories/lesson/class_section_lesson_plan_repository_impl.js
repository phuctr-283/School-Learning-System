const ClassSectionLessonPlanRepository = require("../../../domain/repositories/lesson/class_section_lesson_plan_repository");

const lessonApi = require("../../api/lesson/lesson_api");

const ClassSectionLessonPlanDTO = require("../../../application/lessons/dto/class_section_lesson_plan.dto");

class ClassSectionLessonPlanRepositoryImpl extends ClassSectionLessonPlanRepository {
  async getClassSectionLessonPlans(req, courseLessonPlanId) {
    try {
      if (!courseLessonPlanId) {
        throw new Error("Course lesson plan ID không được để trống.");
      }

      const response = await lessonApi.getClassSectionLessonPlans(
        req,
        courseLessonPlanId,
      );

      if (!response?.success) {
        throw new Error(
          response?.message || "Không thể lấy kế hoạch nhóm lớp học phần.",
        );
      }

      const plans = response.data || [];

      return plans.map((item) => new ClassSectionLessonPlanDTO(item));
    } catch (error) {
      console.error(
        "GET CLASS SECTION LESSON PLANS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy kế hoạch nhóm lớp học phần.",
      );
    }
  }
}

module.exports = ClassSectionLessonPlanRepositoryImpl;
