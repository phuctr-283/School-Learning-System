const {
  importClassSectionStudentsUseCase,
} = require("../../../../infrastructure/dependencies/class_section/class_section_student_dependency");

const classSectionStudentController = {
  async renderImportStudent(req, res, next) {
    try {
      return res.render("teacher/import/student", {
        title: "Import sinh viên",

        importSuccess: false,

        error: null,
      });
    } catch (error) {
      next(error);
    }
  },
  async importStudents(req, res, next) {
    try {
      const file = req.file;

      if (!file) {
        return res.status(400).render("teacher/import/student", {
          title: "Import sinh viên",

          importSuccess: false,

          error: "Vui lòng chọn file Excel",
        });
      }

      const result = await importClassSectionStudentsUseCase.execute(req, file);

      return res.status(200).render("teacher/import/student", {
        title: "Import sinh viên",

        importSuccess: true,

        importMessage: result.message,

        subjectName: result.subject_name,

        groupNumber: result.group_number,

        semesterNumber: result.semester_number,

        academicYearName: result.academic_year_name,

        importCount: result.imported_count,

        skippedCount: result.skipped_count,

        notFoundCount: result.not_found_count,

        importedStudents: result.imported,

        skippedStudents: result.skipped,

        notFoundStudents: result.not_found,

        error: null,
      });
    } catch (error) {
      console.error("IMPORT CLASS SECTION STUDENTS ERROR:", error);

      const errorMessage =
        error.response?.data?.message ||
        error.message ||
        "Import sinh viên thất bại";

      return res.status(400).render("teacher/import/student", {
        title: "Import sinh viên",

        importSuccess: false,

        error: errorMessage,
      });
    }
  },
};

module.exports = classSectionStudentController;
