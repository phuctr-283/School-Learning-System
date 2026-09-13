const {
  getUniversitiesUseCase,
  createUniversityUseCase,
} = require(
  "../../../../infrastructure/dependencies/university/university_dependency",
);


class UniversityController {
  async list(req, res) {
    try {
      const universities =
        await getUniversitiesUseCase.execute(req);

      return res.render(
        "super_admin/university/list",
        {
          title: "Danh sách trường",
          universities,
        },
      );
    } catch (error) {
      console.error(
        "GET UNIVERSITIES ERROR:",
        error.message,
      );

      return res.status(500).render(
        "error",
        {
          message: "Không thể tải danh sách trường",
        },
      );
    }
  }

  async getCreateUniversityPage(req, res) {
    return res.render(
      "super_admin/university/create",
      {
        title: "Thêm trường đại học",
        form: {
          university_id: "",
          name: "",
          domain: "",
          email: "",
          phone: "",
        },
        errors: {},
      },
    );
  }

  async createUniversity(req, res) {
    const {
      university_id,
      name,
      domain,
      email,
      phone,
    } = req.body;

    const form = {
      university_id,
      name,
      domain,
      email,
      phone,
    };

    try {
      await createUniversityUseCase.execute(
        form,
        req,
      );

      return res.redirect(
        "/super-admin/university",
      );
    } catch (error) {
      console.error(
        "CREATE UNIVERSITY ERROR:",
        error.message,
      );

      const errors = {
        general:
          error.message ||
          "Không thể tạo trường đại học",
      };

      return res.status(400).render(
        "super_admin/university/create",
        {
          title: "Thêm trường đại học",
          form,
          errors,
          error: errors.general,
        },
      );
    }
  }
}

module.exports = new UniversityController();