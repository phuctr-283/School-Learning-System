const {
  getTeacherClassSectionsUseCase,
} = require("../../../../infrastructure/dependencies/class_section/class_section_dependency");

class ClassSectionController {
  async getClassSectionsAssignment(req, res) {
    try {
      const { subjectId } = req.params;

      const classSections = await getTeacherClassSectionsUseCase.execute(
        req,
        subjectId,
      );

      return res.render("teacher/assignment/group", {
        subjectId,
        classSections,
      });
    } catch (error) {
      console.error(
        "GET TEACHER SUBJECT GROUPS ERROR:",
        error.response?.data || error.message,
      );

      return res.status(error.response?.status || 500).render("error", {
        message:
          error.response?.data?.detail ||
          "Không thể tải danh sách nhóm học phần",
      });
    }
  }
}

module.exports = new ClassSectionController();
