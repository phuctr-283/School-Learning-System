const LessonRepository = require("../../../domain/repositories/lesson/lesson_repository");

const LessonDTO = require("../../../application/lessons/dto/lesson.dto");

const lessonApi = require("../../api/lesson/lesson_api");

class LessonRepositoryImpl extends LessonRepository {
  // =========================================
  // GET LESSONS
  // =========================================

  async getLessons(req) {
    try {
      const response = await lessonApi.getLessons(req);

      if (!response.success) {
        throw new Error(
          response.message || "Không thể lấy danh sách buổi học",
        );
      }

      const lessons = response.data || [];

      return lessons.map(
        (lesson) => new LessonDTO(lesson),
      );
    } catch (error) {
      console.error(
        "GET LESSONS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy danh sách buổi học",
      );
    }
  }

  // =========================================
  // CREATE LESSON
  // =========================================

  async createLesson(req, data) {
    try {
      const response = await lessonApi.createLesson(
        req,
        data,
      );

      if (!response.success) {
        throw new Error(
          response.message || "Không thể tạo buổi học",
        );
      }

      const lessons = response.data || [];

      return lessons.map(
        (lesson) => new LessonDTO(lesson),
      );
    } catch (error) {
      console.error(
        "CREATE LESSON ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể tạo buổi học",
      );
    }
  }
}

module.exports = LessonRepositoryImpl;