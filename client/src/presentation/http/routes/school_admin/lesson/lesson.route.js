const express = require("express");

const router = express.Router();

const lessonController = require("../../../controllers/school_admin/lesson.controller");

router.get("/", lessonController.getLessonPlanPage.bind(lessonController));

router.get(
  "/create/lesson",
  lessonController.createLessonPage.bind(lessonController),
);
router.post(
  "/create/lesson",
  lessonController.createLesson.bind(lessonController),
);

router.get(
  "/create/semester-lesson-plan",
  lessonController.createSemesterLessonPlanPage.bind(lessonController),
);
router.post(
  "/create/semester-lesson-plan",
  lessonController.createSemesterLessonPlan.bind(lessonController),
);

router.get(
  "/create/subject-lesson-plan",
  lessonController.createSubjectLessonPlanPage.bind(lessonController),
);
router.post(
  "/create/subject-lesson-plan",
  lessonController.createSubjectLessonPlan.bind(lessonController),
);

router.get(
  "/course-lesson-plan/:courseLessonPlanId/class-sections",
  lessonController.getClassSectionLessonPlans.bind(lessonController),
);

router.post(
  "/ensure/lesson-plans",
  lessonController.ensureLessonPlans.bind(lessonController),
);

module.exports = router;
