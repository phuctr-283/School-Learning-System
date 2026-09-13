const {
  getUniversityDepartmentsUseCase,
  createDepartmentUseCase,
  getActiveDepartmentsUseCase,
} = require(
  "../../../../infrastructure/dependencies/department/department_dependency",
);


const DepartmentController = {
  async list(req, res) {
    try {
      const departments =
        await getUniversityDepartmentsUseCase.execute(req);

      return res.render(
        "school_admin/university/department/list",
        {
          title: "Danh sách khoa",
          departments,
        },
      );
    } catch (error) {
      console.error(
        "GET DEPARTMENTS CONTROLLER ERROR:",
        error.message,
      );

      return res.render(
        "school_admin/university/department/list",
        {
          title: "Danh sách khoa",
          departments: [],
          error: error.message,
        },
      );
    }
  },

  async showCreate(req, res) {
    return res.render(
      "school_admin/university/department/create",
      {
        title: "Thêm khoa",
      },
    );
  },

  async create(req, res) {
    try {
      await createDepartmentUseCase.execute(
        req,
        req.body,
      );

      return res.redirect(
        "/school-admin/university/departments",
      );
    } catch (error) {
      console.error(
        "CREATE DEPARTMENT CONTROLLER ERROR:",
        error.message,
      );

      return res.render(
        "school_admin/university/department/create",
        {
          title: "Thêm khoa",
          error: error.message,
          department: {
            department_id: req.body.department_id,
            department_number:
              req.body.department_number,
            name: req.body.name,
            head_id: req.body.head_id,
          },
        },
      );
    }
  },

  async getActiveDepartments(req, res) {
    try {
      const {
        university_id: universityId,
      } = req.query;

      if (!universityId) {
        return res.status(400).json({
          success: false,
          message: "Thiếu university_id",
        });
      }

      const departments =
        await getActiveDepartmentsUseCase.execute(
          universityId,
        );

      return res.status(200).json({
        success: true,
        data: departments,
      });
    } catch (error) {
      console.error(
        "GET REGISTER DEPARTMENTS ERROR:",
        error.message,
      );

      return res.status(
        error.response?.status || 500,
      ).json({
        success: false,
        message:
          error.response?.data?.message ||
          error.message ||
          "Không thể lấy danh sách khoa",
      });
    }
  },
};

module.exports = DepartmentController;