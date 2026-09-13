const LessonOpeningRepository = require("../../../domain/repositories/lesson/lesson_opening_repository");

const lessonOpeningApi = require("../../api/lesson/lesson_api");

const LessonOpeningContentDTO = require("../../../application/lessons/dto/lesson_opening_content.dto");

class LessonOpeningRepositoryImpl extends LessonOpeningRepository {
  async ensureLessonOpenings(req) {
    const response = await lessonOpeningApi.ensureLessonOpenings(req);

    if (!response || response.success !== true) {
      throw new Error(response?.message || "Không thể tạo danh sách buổi học.");
    }

    const data = Array.isArray(response.data) ? response.data : [];

    return data.map((item) => LessonOpeningContentDTO.fromResponse(item));
  }

  async getLessonOpenings(req, classSectionLessonPlanId) {
    const response = await lessonOpeningApi.getLessonOpenings(
      req,
      classSectionLessonPlanId,
    );

    if (!response || response.success !== true) {
      throw new Error(response?.message || "Không thể tải danh sách buổi học.");
    }

    const data = Array.isArray(response.data) ? response.data : [];

    return data.map((item) => LessonOpeningContentDTO.fromResponse(item));
  }
}

module.exports = LessonOpeningRepositoryImpl;
