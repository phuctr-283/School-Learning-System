const express = require("express");
const router = express.Router();

const lessonController = require("../../../controllers/student/lesson.controller")

router.get("/lessons/:classSectionId",lessonController.getLessonOpenings.bind(lessonController) );
module.exports = router;
