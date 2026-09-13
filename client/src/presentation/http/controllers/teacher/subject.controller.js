const {
  getTeacherSubjectsUseCase,
} = require("../../../../infrastructure/dependencies/class_section/class_section_dependency");

class SubjectController {
  async getSubjectsAssignment(req, res) {
    try {
      const subjects = await getTeacherSubjectsUseCase.execute(req);

      return res.render("teacher/assignment/subject", {
        title:"Bài tập",
        subjects,
      });
    } catch (error) {
      console.error(
        "GET TEACHER SUBJECTS ERROR:",
        error.response?.data || error.message,
      );

      return res.status(error.response?.status || 500).render("error", {
        message:
          error.response?.data?.detail || "Không thể tải danh sách môn học",
      });
    }
  }
}

module.exports = new SubjectController();
