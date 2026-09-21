const express = require("express");
const router = express.Router();

const lessonOpeningController = require("../../../controllers/teacher/lesson_opening.controller");

router.get(
  "/class-sections/:classSectionId/lessons",
  lessonOpeningController.getLessonOpenings.bind(lessonOpeningController),
);
router.patch(
  "/class-sections/:classSectionLessonPlanId/:lessonId/status",
  lessonOpeningController.updateLessonOpeningStatus.bind(
    lessonOpeningController,
  ),
);

router.get(
  "/lesson-opening/class-sections",
  lessonOpeningController.getClassSections.bind(lessonOpeningController),
);

router.get(
  "/lesson-opening/lessons",
  lessonOpeningController.getLessonOpeningsBySelection.bind(
    lessonOpeningController,
  ),
);
router.post(
  "/lesson-opening/apply-assignment",
  lessonOpeningController.applyAssignment.bind(lessonOpeningController),
);
router.get(
  "/lesson-opening/applications",
  lessonOpeningController.getAssignmentApplications.bind(
    lessonOpeningController,
  ),
);
router.patch(
  "/applications/:applicationId/class-sections/:classSectionId/status",
  lessonOpeningController.updateAssignmentApplicationClassSectionStatus.bind(
    lessonOpeningController,
  ),
);
router.get(
  "/lesson-opening/:assignment_id",
  lessonOpeningController.showLessonOpeningApplicationPage.bind(
    lessonOpeningController,
  ),
);

module.exports = router;
