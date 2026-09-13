const {
  getActiveUniversitiesUseCase,
} = require(
  "../../../../infrastructure/dependencies/university/university_dependency",
);

const {
  getActiveDepartmentsUseCase,
} = require(
  "../../../../infrastructure/dependencies/department/department_dependency",
);

const {
  registerTeacherUseCase,
} = require(
  "../../../../infrastructure/dependencies/teacher/teacher_dependency",
);


class RegisterController {
  async register(req, res) {
    try {
      await registerTeacherUseCase.execute(
        req.body,
      );

      return res.redirect(
        "/?registered=true",
      );
    } catch (error) {
      console.error(
        "REGISTER CONTROLLER ERROR:",
        error.message,
      );

      let universities = [];
      let departments = [];

      try {
        universities =
          await getActiveUniversitiesUseCase.execute();
      } catch (universityError) {
        console.error(
          "GET UNIVERSITIES AFTER REGISTER ERROR:",
          universityError.message,
        );
      }

      if (req.body.university_id) {
        try {
          departments =
            await getActiveDepartmentsUseCase.execute(
              req.body.university_id,
            );
        } catch (departmentError) {
          console.error(
            "GET DEPARTMENTS AFTER REGISTER ERROR:",
            departmentError.message,
          );
        }
      }

      return res.status(400).render(
        "authentication/index",
        {
          title: "Đăng ký tài khoản",
          authentication: true,
          authMode: "login",
          universities,
          departments,
          error: error.message,
          formData: req.body,
        },
      );
    }
  }
}

module.exports = new RegisterController();