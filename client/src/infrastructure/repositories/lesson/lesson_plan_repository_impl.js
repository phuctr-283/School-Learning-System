const LessonPlanRepository = require("../../../domain/repositories/lesson/lesson_plan_repository");

const lessonApi = require("../../api/lesson/lesson_api");

const CourseLessonPlanDTO = require("../../../application/lessons/dto/course_lesson_plan.dto");

const ClassSectionLessonPlanDTO = require("../../../application/lessons/dto/class_section_lesson_plan.dto");

class LessonPlanRepositoryImpl extends LessonPlanRepository {
  async ensureLessonPlans(req, config = {}) {
    try {
      const response = await lessonApi.ensureLessonPlans(req, config);

      console.log(
        "ENSURE LESSON PLANS RESPONSE:",
        JSON.stringify(response, null, 2),
      );

      if (!response?.success) {
        throw new Error(response?.message || "Không thể tạo kế hoạch bài học.");
      }

      const data = response?.data ?? {};

      const courseLessonPlans = (data.course_lesson_plans ?? []).map(
        (item) => new CourseLessonPlanDTO(item),
      );

      const classSectionLessonPlans = (
        data.class_section_lesson_plans ?? []
      ).map((item) => new ClassSectionLessonPlanDTO(item));

      return {
        courseLessonPlans,
        classSectionLessonPlans,
      };
    } catch (error) {
      console.error("ENSURE LESSON PLANS ORIGINAL ERROR:", error);

      console.error("STATUS:", error?.response?.status);

      console.error("DATA:", error?.response?.data);

      console.error("MESSAGE:", error?.message);

      const message =
        error?.response?.data?.message ||
        error?.response?.data?.detail ||
        error?.message ||
        "Không thể tạo kế hoạch bài học.";

      const newError = new Error(message);

      newError.status = error?.response?.status || 500;

      throw newError;
    }
  }
}

module.exports = LessonPlanRepositoryImpl;
