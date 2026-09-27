const {
  getStudentLessonOpeningsUseCase,
} = require("../../../../infrastructure/dependencies/lesson/lesson_dependency");

class LessonController {
  async getLessonOpenings(req, res) {
    const classSectionId = String(req.params.classSectionId || "").trim();

    if (!classSectionId) {
      return res.status(400).render("errors/400", {
        title: "Thông tin không hợp lệ",
        message: "Không đủ thông tin để tải buổi học.",
        blank: true,
      });
    }

    try {
      console.log("CLASS SECTION ID: ", classSectionId);
      console.log("CLASS SECTION ID TYPE: ", typeof classSectionId);
      const lessons = await getStudentLessonOpeningsUseCase.execute(
        req,
        classSectionId,
      );
      console.log("LESSONS", lessons);
      return res.render("student/assignment/lesson", {
        title: "Bài tập",
        classSectionId,
        lessons,
      });
    } catch (error) {
      const errorStatus =
        Number(error.status) || Number(error.response?.status) || 500;

      const message = error.message || "Không thể tải danh sách buổi học.";

      return res.status(errorStatus).render(`errors/${errorStatus}`, {
        title: "Không thể tải dữ liệu",
        message,
        blank: true,
      });
    }
  }
}

module.exports = new LessonController();
