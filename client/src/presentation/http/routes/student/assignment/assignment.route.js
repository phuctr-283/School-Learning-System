const express = require("express");
const router = express.Router();

const classSectionRouter = require("../class_section/class_section.route");
const lessonRouter = require("../lesson/lesson.route")
const assignmentController = require("../../../controllers/student/assignment.controller");

router.get("/class-sections/:classSectionId/lessons/:lessonId/assignment", assignmentController.getAssignmentApplications.bind(assignmentController));
router.use("/", classSectionRouter);
router.use("/", lessonRouter);
module.exports = router;
