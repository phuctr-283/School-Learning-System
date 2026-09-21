const LessonOpeningRepository = require("../../../domain/repositories/lesson/lesson_opening_repository");

const lessonOpeningApi = require("../../api/lesson/lesson_api");

const LessonOpeningContentDTO = require("../../../application/lessons/dto/lesson_opening_content.dto");

class LessonOpeningRepositoryImpl extends LessonOpeningRepository {

  async getLessonOpenings(req, classSectionId) {
    const response = await lessonOpeningApi.getLessonOpenings(
      req,
      classSectionId,
    );

    if (!response || response.success !== true) {
      throw new Error(response?.message || "Không thể tải danh sách buổi học.");
    }

    const data = Array.isArray(response.data) ? response.data : [];

    return data.map((item) => LessonOpeningContentDTO.fromResponse(item));
  }
  async updateStatus(req, classSectionLessonPlanId, lessonId, status) {
    const response = await lessonOpeningApi.updateStatus(
      req,
      classSectionLessonPlanId,
      lessonId,
      status,
    );

    return response;
  }
}

module.exports = LessonOpeningRepositoryImpl;
