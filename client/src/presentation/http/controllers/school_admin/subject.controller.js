const {
  getSubjectsUseCase,
  createSubjectUseCase,
} = require("../../../../infrastructure/dependencies/subject/subject_dependency");
const {
  getActivesDepartmentsUseCase,
} = require("../../../../infrastructure/dependencies/department/department_dependency");
const subjectController = {
  // =========================================
  // GET SUBJECT LIST PAGE
  // =========================================

  async list(req, res) {
    try {
      const subjects = await getSubjectsUseCase.execute(req);

      return res.render("school_admin/university/subject/list", {
        title: "Danh sách môn học",
        subjects,
      });
    } catch (error) {
      console.error("GET SUBJECT PAGE ERROR:", error.message);

      return res.status(500).render("school_admin/university/subject/list", {
        title: "Danh sách môn học",
        subjects: [],
        error: error.message,
      });
    }
  },
  async showCreate(req, res) {
    try {
      const departments = await getActivesDepartmentsUseCase.execute(req);
      return res.render("school_admin/university/subject/create", {
        title: "Thêm mới môn học",
        departments,
      });
    } catch (error) {
      console.error("GET DEPARTMENTS FOR SUBJECT ERROR:", error.message);
      return res.status(500).render("error", {
        message: error.message,
      });
    }
  },
  async create(req, res) {
    try {
      await createSubjectUseCase.execute(req, req.body);

      return res.redirect("/school-admin/university/subjects");
    } catch (error) {
      console.error("CREATE SUBJECT CONTROLLER ERROR:", error.message);

      let departments = [];

      try {
        departments = await getActiveDepartmentsUseCase.execute(req);
      } catch (_) {}

      return res.status(400).render("school_admin/university/subject/create", {
        title: "Thêm môn học",
        departments,
        formData: req.body,
        error: error.message,
      });
    }
  },
};

module.exports = subjectController;
