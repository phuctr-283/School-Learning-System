const express = require("express");
const router = express.Router();
const assignmentController = require("../../../controllers/student/assignment.controller");
const assignmentQrController = require("../../../controllers/student/assignment_qr.controller")
const assignmentAccessMiddleware = require("../../../middlewares/assignment_qr_access_middleware");

router.get(
  "/student/assignment/qr",
  assignmentQrController.assignmentQrEntry.bind(assignmentQrController),
);

router.post(
  "/student/assignment/qr/verify",
  assignmentQrController.verifyStudentAssignmentQr.bind(assignmentQrController),
);
router.get(
  "/student/assignment/take/:assignmentApplicationId",
  assignmentAccessMiddleware,
  assignmentController.takeAssignment.bind(assignmentController),
);

router.post(
  "/student/assignment/take/:assignmentApplicationId/save",
  assignmentAccessMiddleware,
  assignmentController.saveAssignment.bind(assignmentController),
);

router.post(
  "/student/assignment/take/:assignmentApplicationId/submit",
  assignmentAccessMiddleware,
  assignmentController.submitAssignment.bind(assignmentController),
);

module.exports = router;
