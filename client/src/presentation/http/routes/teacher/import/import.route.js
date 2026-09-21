const express = require("express");
const router = express.Router();
const multer = require("multer");
const upload = multer({
  dest: "uploads/",

  limits: {
    fileSize:
      128 * 1024 * 1024,
  },
});
const dashboardController = require("../../../controllers/teacher/dashboard.controller")
const importController = require("../../../controllers/teacher/class_section_student.controller");
router.get("/", dashboardController.showImportPage.bind(dashboardController));
router.get("/students", importController.renderImportStudent.bind(importController));
router.post("/students",upload.single("file"), importController.importStudents.bind(importController));
module.exports = router;
