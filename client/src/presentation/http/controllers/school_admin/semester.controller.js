const {
  getSemestersUseCase,
  createSemesterUseCase,
} = require("../../../../infrastructure/dependencies/semester/semester_dependency");
const {
  getActiveAndPlannedAcademicYearsUseCase,
} = require("../../../../infrastructure/dependencies/academic_year/academic_year_dependency");

const SemesterController = {
  async list(req, res) {
    try {
      const semesters = await getSemestersUseCase.execute(req);

      return res.render("school_admin/university/semester/list", {
        title: "Quản lý học kỳ",
        semesters,
      });
    } catch (error) {
      console.error("GET SEMESTERS CONTROLLER ERROR:", error.message);

      return res.status(500).render("school_admin/semester/list", {
        title: "Quản lý học kỳ",
        semesters: [],
        error: error.message,
      });
    }
  },
  async showCreate(req, res) {
    try {
      const academicYears =
        await getActiveAndPlannedAcademicYearsUseCase.execute(req);

      return res.render("school_admin/university/semester/create", {
        title: "Thêm học kỳ",
        academicYears,
        formData: {},
      });
    } catch (error) {
      console.error("GET CREATE SEMESTER PAGE ERROR:", error.message);

      return res.status(500).render("school_admin/university/semester/create", {
        title: "Thêm học kỳ",
        academicYears: [],
        formData: {},
        error: error.message,
      });
    }
  },
  async create(req, res) {
    try {
      await createSemesterUseCase.execute(req, req.body);

      return res.redirect("/school-admin/university/semesters");
    } catch (error) {
      console.error("CREATE SEMESTER CONTROLLER ERROR:", error.message);

      let academicYears = [];

      try {
        academicYears =
          await getActiveAndPlannedAcademicYearsUseCase.execute(req);
      } catch (_) {}

      return res.status(400).render("school_admin/university/semester/create", {
        title: "Thêm học kỳ",

        academicYears,

        formData: req.body,

        error: error.message,
      });
    }
  },
};

module.exports = SemesterController;
