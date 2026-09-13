const express = require("express");
const router = express.Router();

const dashboardRouter = require("./teacher/dashboard/dashboard.route");
const assignmentRouter = require("./teacher/assignment/assignment.route");

const authMiddleware = require("../middlewares/auth.middleware");
const requireAccountLevel = require("../middlewares/require_account_level");
const AccountLevel = require("../../../domain/enums/account_level");


router.use(authMiddleware, requireAccountLevel(AccountLevel.TEACHER));

router.use("/", dashboardRouter);
router.use("/assignment", assignmentRouter);
module.exports = router;
