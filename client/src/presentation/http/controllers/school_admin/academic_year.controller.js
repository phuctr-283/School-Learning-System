const {
  getAcademicYearsUseCase,
  createAcademicYearUseCase,
} = require(
  "../../../../infrastructure/dependencies/academic_year/academic_year_dependency",
);


const AcademicYearController = {
  async list(req, res) {
    try {
      const academicYears =
        await getAcademicYearsUseCase.execute(req);

      return res.render(
        "school_admin/university/academic_year/list",
        {
          title: "Năm học",
          academicYears,
        },
      );
    } catch (error) {
      console.error(
        "ACADEMIC YEAR LIST CONTROLLER ERROR:",
        error.message,
      );

      return res.status(400).render(
        "school_admin/university/academic_year/list",
        {
          title: "Năm học",
          academicYears: [],
          error: error.message,
        },
      );
    }
  },

  async showCreate(req, res) {
    return res.render(
      "school_admin/university/academic_year/create",
      {
        title: "Tạo năm học",
      },
    );
  },

  async create(req, res) {
    try {
      await createAcademicYearUseCase.execute(
        req,
        req.body,
      );

      return res.redirect(
        "/school-admin/university/academic-years",
      );
    } catch (error) {
      console.error(
        "CREATE ACADEMIC YEAR CONTROLLER ERROR:",
        error.message,
      );

      return res.status(400).render(
        "school_admin/university/academic_year/create",
        {
          title: "Thêm năm học",
          error: error.message,
          formData: req.body,
        },
      );
    }
  },
};

module.exports = AcademicYearController;