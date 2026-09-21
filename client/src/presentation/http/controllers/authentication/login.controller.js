const {
  loginUserUseCase,
} = require(
  "../../../../infrastructure/dependencies/auth/auth_dependency",
);

const {
  getActiveUniversitiesUseCase,
} = require(
  "../../../../infrastructure/dependencies/university/university_dependency",
);

const {getActiveDepartmentsUseCase} = require("../../../../infrastructure/dependencies/department/department_dependency")
const TokenManager = require(
  "../../../../infrastructure/security/token_manager",
);

const AccountLevel = require(
  "../../../../domain/enums/account_level",
);


class LoginController {
  async showAuthentication(req, res) {
    try {
      const universities =
        await getActiveUniversitiesUseCase.execute();

      const role = req.query.role;

      if (role === "admin") {
        return res.render("authentication/index", {
          title: "Đăng ký quản trị viên",
          authentication: true,
          authMode: "admin-register",
        });
      }

      return res.render("authentication/index", {
        title: "Đăng nhập tài khoản",
        authentication: true,
        authMode: "login",
        universities,
        departments: [],
      });
    } catch (error) {
      console.error(
        "SHOW REGISTER ERROR:",
        error.message,
      );

      return res.render("authentication/index", {
        title: "Đăng nhập tài khoản",
        authentication: true,
        authMode: "login",
        universities: [],
        departments: [],
        error: error.message,
      });
    }
  }
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
  }
  async login(req, res) {
    const {
      username,
      password,
    } = req.body;

    try {
      const result =
        await loginUserUseCase.execute({
          username,
          password,
        });

      const user = result.user;

      TokenManager.setTokens(
        req.session,
        {
          access_token: result.access_token,
          refresh_token: result.refresh_token,
        },
      );

      req.session.user = user;

      switch (user.account_level) {
        case AccountLevel.SUPER_ADMIN:
          return res.redirect("/super-admin");

        case AccountLevel.SCHOOL_ADMIN:
          return res.redirect("/school-admin");

        case AccountLevel.TEACHER:
          return res.redirect("/teacher");

        case AccountLevel.STUDENT:
          return res.redirect("/student");

        default:
          throw new Error(
            "Account level không hợp lệ",
          );
      }
    } catch (error) {
      console.error(
        "LOGIN ERROR:",
        error.message,
      );

      return res.status(401).render(
        "authentication/index",
        {
          title: "Đăng nhập tài khoản",
          error: error.message,
          username: username || "",
          authentication: true,
          authMode: "login",
        },
      );
    }
  }
}

module.exports = new LoginController();