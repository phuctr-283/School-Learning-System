const UsernamePolicy = require(
  "../../../../../domain/services/username_policy",
);

const {
  registerSuperAdminUseCase,
} = require(
  "../../../../../infrastructure/dependencies/super_admin/super_admin_dependency",
);


class SuperAdminController {
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

      if (
        !UsernamePolicy.validateSuperAdmin(
          normalizedUsername,
        )
      ) {
        throw new Error(
          "Username Super Admin phải có dạng @admin.vn",
        );
      }

      await registerSuperAdminUseCase.execute({
        req,
        full_name,
        username: normalizedUsername,
        password,
      });

      return res.redirect("/");
    } catch (error) {
      console.error(
        "REGISTER SUPER ADMIN ERROR:",
        error.message,
      );

      return res.status(400).render(
        "authentication/index",
        {
          title: "Đăng ký Super Admin",
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

module.exports = new SuperAdminController();