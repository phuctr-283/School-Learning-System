const express = require("express");

const router = express.Router();

const importClassSectionRouter = require("./class_section/import_class_section.route")
const importStudentRouter = require("./student/import_student.route");
const dashboardController = require("../../controllers/school_admin/dashboard.controller");

router.get("/", dashboardController.showImportPage.bind(dashboardController));
router.use("/students", importStudentRouter);
router.use("/class-sections", importClassSectionRouter);


module.exports = router;