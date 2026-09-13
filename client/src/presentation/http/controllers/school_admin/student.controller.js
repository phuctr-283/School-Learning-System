const {
  getUniversityStudentsUseCase,
  importStudentsUseCase,
} = require("../../../../infrastructure/dependencies/student/student_dependency");

const studentController = {
  async list(req, res) {
    try {
      const students = await getUniversityStudentsUseCase.execute(req);

      return res.render("school_admin/student/list", {
        title: "Danh sách sinh viên",
        students,
      });
    } catch (error) {
      console.error("GET STUDENTS PAGE ERROR:", error.message);

      return res.status(500).render("school_admin/student/list", {
        title: "Danh sách sinh viên",
        students: [],
        error: error.message,
      });
    }
  },
  async importStudentPage(req, res) {
    return res.render("school_admin/import/student", {
      title: "Import sinh viên",
      importSuccess: false,
      importMessage: null,
      importCount: 0,
      error: null,
    });
  },

  async importStudents(req, res) {
    try {
      if (!req.file) {
        throw new Error("Vui lòng chọn file Excel.");
      }

      const result = await importStudentsUseCase.execute(req, req.file);

      return res.render("school_admin/import/student", {
        title: "Import sinh viên",
        importSuccess: true,
        importMessage: "Dữ liệu sinh viên đã được nhập thành công.",
        importCount: result.created_count || 0,
        error: null,
      });
    } catch (error) {
      console.error("IMPORT STUDENTS CONTROLLER ERROR:", error.message);

      return res.status(400).render("school_admin/import/student", {
        title: "Import sinh viên",
        importSuccess: false,
        importMessage: null,
        importCount: 0,
        error: error.message,
      });
    }
  },
};

module.exports = studentController;
