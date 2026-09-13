const express = require("express");
const router = express.Router();

const dashboardRouter = require("./school_admin/dashboard/dashboard.route");
const universityRouter = require("./school_admin/university.route");
const studentRouter = require("./school_admin/student/student.route");
const teacherRouter = require("./school_admin/teacher/teacher.route");
const importRouter = require("./school_admin/import.route")

const authMiddleware = require("../middlewares/auth.middleware");
const requireAccountLevel = require("../middlewares/require_account_level");
const AccountLevel = require("../../../domain/enums/account_level");


router.use(authMiddleware, requireAccountLevel(AccountLevel.SCHOOL_ADMIN));

router.use("/", dashboardRouter);
router.use("/university", universityRouter);
router.use("/students", studentRouter);
router.use("/teachers", teacherRouter);
router.use("/imports", importRouter);
module.exports = router;
