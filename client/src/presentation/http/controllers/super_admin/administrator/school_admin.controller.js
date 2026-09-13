const UsernamePolicy = require(
  "../../../../../domain/services/username_policy",
);

const {
  getSchoolAdminsUseCase,
  registerSchoolAdminUseCase,
} = require(
  "../../../../../infrastructure/dependencies/school_admin/school_admin_dependency",
);


class SchoolAdminController {
  async list(req, res) {
    try {
      const admins =
        await getSchoolAdminsUseCase.execute(req);

      return res.render(
        "super_admin/school_admin/list",
        {
          title: "Danh sách Admin",
          admins,
        },
      );
    } catch (error) {
      console.error(
        "GET SCHOOL ADMINS ERROR:",
        error.message,
      );

      return res.status(500).render(
        "error",
        {
          message: "Không thể tải danh sách Admin",
        },
      );
    }
  }

  async register(req, res) {
    const {
      full_name,
      username,
      password,
      confirmPassword,
    } = req.body;

    const form = {
      full_name: full_name || "",
      username: username || "",
      password: "",
      confirmPassword: "",
    };

    try {
      if (password !== confirmPassword) {
        throw new Error(
          "Mật khẩu xác nhận không khớp",
        );
      }

      const normalizedUsername =
        UsernamePolicy.normalize(
          username || "",
        );

      const universityDomain =
        UsernamePolicy.extractSchoolDomain(
          normalizedUsername,
        );

      if (!universityDomain) {
        throw new Error(
          "Username School Admin không đúng định dạng",
        );
      }

      await registerSchoolAdminUseCase.execute({
        req,
        full_name,
        username: normalizedUsername,
        password,
        universityDomain,
      });

      return res.redirect("/");
    } catch (error) {
      console.error(
        "REGISTER SCHOOL ADMIN ERROR:",
        error.message,
      );

      return res.status(400).render(
        "authentication/index",
        {
          title: "Đăng ký School Admin",
          authentication: true,
          authMode: "admin-register",
          form,
          errors: {
            general: error.message,
          },
          error: error.message,
        },
      );
    }
  }
}

module.exports = new SchoolAdminController();