const {
  getUniversityTeachersUseCase,
} = require(
  "../../../../infrastructure/dependencies/teacher/teacher_dependency",
);


const TeacherController = {
  async list(req, res) {
    try {
      const teachers =
        await getUniversityTeachersUseCase.execute(req);

      return res.render(
        "school_admin/teacher/list",
        {
          title: "Danh sách giảng viên",
          teachers,
        },
      );
    } catch (error) {
      console.error(
        "GET TEACHERS CONTROLLER ERROR:",
        error.message,
      );

      return res.render(
        "school_admin/teacher/list",
        {
          title: "Danh sách giảng viên",
          teachers: [],
          error: error.message,
        },
      );
    }
  },
};

module.exports = TeacherController;