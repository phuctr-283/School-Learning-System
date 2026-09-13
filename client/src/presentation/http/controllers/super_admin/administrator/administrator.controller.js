const UsernamePolicy = require("../../../../../domain/services/username_policy");

const SchoolAdminController = require("./school_admin.controller");
const SuperAdminController = require("./super_admin.controller");

class AdministratorController {
  async register(req, res) {
    const username = UsernamePolicy.normalize(req.body.username || "");
    if (UsernamePolicy.validateSuperAdmin(username)) {
      return SuperAdminController.register(req, res);
    }
    const universityDomain = UsernamePolicy.extractSchoolDomain(username);

    if (universityDomain) {
      return SchoolAdminController.register(req, res);
    }
    return res.status(400).render("auth/index", {
      title: "Đăng ký Admin",
      authentication: true,
      authMode: "admin-register",
      form: {
        full_name: req.body.full_name || "",
        username: req.body.username || "",
        password: "",
        confirmPassword: "",
      },
      errors: {
        username: "Username không đúng định dạng Admin",
      },
      error: "Username không đúng định dạng Admin",
    });
  }
}

module.exports = new AdministratorController();
