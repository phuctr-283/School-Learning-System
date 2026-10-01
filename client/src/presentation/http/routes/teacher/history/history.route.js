const express = require("express");
const router = express.Router();
const assignmentController = require("../../../controllers/teacher/assignment.controller");
const subjectController = require("../../../controllers/teacher/subject.controller");
const classSectionController = require("../../../controllers/teacher/class_section.controller")
const lessonController = require("../../../controllers/teacher/lesson_opening.controller")
router.get("/", subjectController.getSubjectHistory.bind(subjectController))
router.get("/subjects/:subjectId/class-sections", classSectionController.getClassSectionHistory.bind(classSectionController))
router.get("/class-sections/:classSectionId/lessons", lessonController.getLessonHistory.bind(lessonController));
router.get(
  "/application/:assignmentApplicationId/students",
  assignmentController.showStudentAttemptsPage.bind(
    assignmentController,
  ),
);
module.exports = router;    