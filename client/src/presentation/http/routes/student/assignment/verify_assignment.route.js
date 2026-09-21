const express = require("express");
const router = express.Router();
const assignmentController = require("../../../controllers/student/assignment.controller");
const assignmentAccessMiddleware = require("../../..//middlewares/assignment_qr_access_middleware");
router.get("/assignment/qr", assignmentController.assignmentQrEntry.bind(assignmentController));

router.post(
  "/assignment/qr/verify",
  assignmentController.verifyStudentAssignmentQr.bind(assignmentController),
);
router.get(
    "/assignment/take/:assignmentApplicationId",
    assignmentAccessMiddleware,
    assignmentController.takeAssignment.bind(
        assignmentController
    )
);


router.post(
    "/assignment/take/:assignmentApplicationId/save",
    assignmentAccessMiddleware,
    assignmentController.saveAssignment.bind(
        assignmentController
    )
);


router.post(
    "/assignment/take/:assignmentApplicationId/submit",
    assignmentAccessMiddleware,
    assignmentController.submitAssignment.bind(
        assignmentController
    )
);

module.exports = router;
