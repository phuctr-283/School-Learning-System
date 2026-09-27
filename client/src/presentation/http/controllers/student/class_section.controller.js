const {
  getStudentClassSectionsUseCase,
} = require("../../../../infrastructure/dependencies/class_section/class_section_dependency");

const studentController = {
  async classSectionStudentPage(req, res) {
    try {
      const classSections= await getStudentClassSectionsUseCase.execute(req);

      return res.render("student/assignment/class_section", {
        title: "Bài tập",
        classSections,
      });
    } catch (error) {
      console.error("GET STUDENT CLASS SECTIONS ERROR:", error.message);

      return res.render("student/assignment/class_section", {
        title: "Bài tập",
        classSections: [],
        error: "Không thể tải danh sách lớp học phần",
      });
    }
  },
};

module.exports = studentController;
