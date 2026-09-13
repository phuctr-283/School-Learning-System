const express = require("express");
const router = express.Router();

const classSectionController = require("../../../controllers/teacher/class_section.controller");

router.get("/subjects/:subjectId/class-sections", classSectionController.getClassSectionsAssignment.bind(classSectionController))

module.exports = router;
