const {
  ensureLessonOpeningsUseCase,
  getLessonOpeningsUseCase,
} = require("../../../infrastructure/dependencies/lesson_opening_dependency");

class LessonOpeningController {
  async ensureLessonOpenings(req, res) {
    try {
      const lessonOpenings = await ensureLessonOpeningsUseCase.execute(req);

      return res.status(200).json({
        success: true,

        message: "Đảm bảo danh sách buổi học thành công.",

        createdCount: lessonOpenings.length,

        data: lessonOpenings,
      });
    } catch (error) {
      return res.status(400).json({
        success: false,

        message: error.message,
      });
    }
  }

  async getLessonOpenings(req, res) {
    try {
      const { classSectionLessonPlanId } = req.params;

      const lessonOpenings = await getLessonOpeningsUseCase.execute(
        req,
        classSectionLessonPlanId,
      );

      return res.status(200).json({
        success: true,

        data: lessonOpenings,
      });
    } catch (error) {
      return res.status(400).json({
        success: false,

        message: error.message,
      });
    }
  }
}

module.exports = new LessonOpeningController();
