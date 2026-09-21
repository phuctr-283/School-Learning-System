const express = require("express");
const router = express.Router();

const assignmentController = require("../../../controllers/teacher/assignment.controller");
const subjectRouter = require("../subject/subject.route");
const classSectionRouter = require("../class_section/class_section.route");
const lessonRouter = require("../lesson/lesson.route");

router.get("/", assignmentController.getIndex.bind(assignmentController));
router.get(
  "/list",
  assignmentController.showAssignmentList.bind(assignmentController),
);
router.get(
  "/list/:subjectId",
  assignmentController.showAssignmentsBySubject.bind(assignmentController),
);
router.get(
  "/create",
  assignmentController.createAssignmentPage.bind(assignmentController),
);
router.post(
  "/create",
  assignmentController.createAssignment.bind(assignmentController),
);
router.use("/", subjectRouter);
router.use("/", classSectionRouter);
router.use("/", lessonRouter);
module.exports = router;
