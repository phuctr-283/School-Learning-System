const express = require("express");
const router = express.Router();

const subjectController = require("../../../controllers/teacher/subject.controller");

router.get("/subjects", subjectController.getSubjectsAssignment.bind(subjectController))

module.exports = router;    