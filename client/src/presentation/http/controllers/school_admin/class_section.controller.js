const {
  getClassSectionsUseCase,
  importClassSectionUseCase,
} = require("../../../../infrastructure/dependencies/class_section/class_section_dependency");

const classSectionController = {
  async list(req, res) {
    try {
      const classSections = await getClassSectionsUseCase.execute(req);

      return res.render("school_admin/university/class_section/list", {
        title: "Danh sách lớp học phần",
        classSections,
      });
    } catch (error) {
      console.error("GET CLASS SECTIONS PAGE ERROR:", error.message);

      return res
        .status(500)
        .render("school_admin/university/class_section/list", {
          title: "Danh sách lớp học phần",
          classSections: [],
          error: error.message,
        });
    }
  },
  async importClassSectionPage(req, res) {
    return res.render("school_admin/import/class_section", {
      title: "Import lớp học phần",
      importSuccess: false,

      importMessage: null,

      importCount: 0,

      skippedCount: 0,
      error: null,
    });
  },
  async importClassSections(req, res) {
    try {
      const result = await importClassSectionUseCase.execute(req, req.file);
      const createdCount = result.createdCount || 0;

      const skippedCount = result.skippedCount || 0;
      let importMessage;

      if (createdCount > 0 && skippedCount > 0) {
        importMessage =
          `Import lớp học phần thành công. ` +
          `Đã tạo ${createdCount} lớp học phần mới, ` +
          `${skippedCount} lớp học phần đã tồn tại ` +
          `nên được bỏ qua.`;
      } else if (createdCount > 0 && skippedCount === 0) {
        importMessage =
          `Import lớp học phần thành công. ` +
          `Đã tạo ${createdCount} lớp học phần mới.`;
      } else if (createdCount === 0 && skippedCount > 0) {
        importMessage =
          `Không có lớp học phần mới được tạo. ` +
          `Có ${skippedCount} lớp học phần ` +
          `đã tồn tại và được bỏ qua.`;
      } else {
        importMessage = "File không có dữ liệu lớp học phần mới.";
      }
      return res.render("school_admin/import/class_section", {
        title: "Import lớp học phần",

        importSuccess: true,

        importMessage,

        importCount: createdCount,

        skippedCount,


        error: null,
      });
    } catch (error) {
      console.error("IMPORT CLASS SECTION CONTROLLER ERROR:", error.message);
      return res.status(400).render("school_admin/import/class_section", {
        title: "Import lớp học phần",
        importSuccess: false,
        importMessage: null,
        importCount: 0,
        skippedCount: 0,
        error: error.message,
      });
    }
  },
};

module.exports = classSectionController;
