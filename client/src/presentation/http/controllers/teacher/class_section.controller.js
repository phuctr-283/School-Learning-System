const {
  getTeacherClassSectionsUseCase,
  getTeacherActivePlannedSubjectsUseCase,
} = require("../../../../infrastructure/dependencies/class_section/class_section_dependency");

class ClassSectionController {
  async getClassSectionsAssignment(req, res) {
    try {
      const { subjectId } = req.params;

      const groups = await getTeacherClassSectionsUseCase.execute(
        req,
        subjectId,
      );

      return res.render("teacher/assignment/group", {
        subjectId,
        groups,
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
  async getTeacherActivePlannedSubjects(req, res) {
    try {
      const { academicYearId, semesterId } = req.query;

      const subjects = await getTeacherActivePlannedSubjectsUseCase.execute(
        req,
        {
          academicYearId,
          semesterId,
        },
      );

      return res.status(200).json({
        success: true,

        data: subjects,
      });
    } catch (error) {
      console.error("[NODE] GET TEACHER SUBJECTS ERROR:", error);

      return res.status(error.response?.status || 400).json({
        success: false,

        message:
          error.response?.data?.message ||
          error.message ||
          "Không thể tải danh sách môn học.",
      });
    }
  }
  async getTeacherActivePlannedClassSections(req, res) {
    try {
      const { subjectId } = req.params;

      const { academicYearId, semesterId } = req.query;

      const classSections = await getTeacherClassSectionsUseCase.execute(req, {
        subjectId,
        academicYearId,
        semesterId,
      });

      return res.status(200).json({
        success: true,

        data: classSections,
      });
    } catch (error) {
      console.error("[NODE] GET TEACHER CLASS SECTIONS ERROR:", error);

      return res.status(error.response?.status || 400).json({
        success: false,

        message:
          error.response?.data?.message ||
          error.message ||
          "Không thể tải danh sách lớp học phần.",
      });
    }
  }
}

module.exports = new ClassSectionController();
