const express = require("express");
const router = express.Router();

const classSectionController = require("../../../controllers/student/class_section.controller")

router.get("/", classSectionController.classSectionStudentPage.bind(classSectionController));

module.exports = router;
