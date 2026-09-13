const express = require("express");
const router = express.Router();

const AcademicYearController = require("../../../controllers/school_admin/academic_year.controller");



router.get("/", AcademicYearController.list.bind(AcademicYearController));
router.get("/create", AcademicYearController.showCreate.bind(AcademicYearController));
router.post("/create", AcademicYearController.create.bind(AcademicYearController));
module.exports = router;
