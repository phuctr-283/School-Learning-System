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
const studentController = require("../../../controllers/school_admin/student.controller");
router.get("/import", studentController.importStudentPage.bind(studentController));
router.post("/import",upload.single("file"), studentController.importStudents.bind(studentController));

module.exports = router;
