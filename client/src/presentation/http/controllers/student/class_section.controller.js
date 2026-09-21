const {
  getStudentClassSectionsUseCase,
} = require("../../../../infrastructure/dependencies/class_section/class_section_dependency");

const studentController = {
  async classSectionStudentPage(req, res) {
    try {
      const subjects = await getStudentClassSectionsUseCase.execute(req);

      return res.render("student/assignment/subject", {
        subjects,
        title: "Bài tập",
      });
    } catch (error) {
      console.error("GET STUDENT CLASS SECTIONS ERROR:", error.message);

      return res.render("student/assignment/subject", {
        subjects: [],
        error: "Không thể tải danh sách lớp học phần",
        title: "Bài tập",
      });
    }
  },
};

module.exports = studentController;
