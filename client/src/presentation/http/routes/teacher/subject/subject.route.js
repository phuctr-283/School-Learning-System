const express = require("express");
const router = express.Router();

const subjectController = require("../../../controllers/teacher/subject.controller");

router.get("/subjects/assignment", subjectController.getSubjectsAssignment.bind(subjectController))
router.get("/history/subjects/history", subjectController.getSubjectHistory.bind(subjectController))
module.exports = router;    