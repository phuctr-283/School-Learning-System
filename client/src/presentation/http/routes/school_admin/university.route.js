const express = require("express");

const router = express.Router();

const departmentRouter = require("./department/department.route");
const academicYearRouter = require("./academic_year/academic_year.route");
const semesterRouter = require("./semester/semester.route");
const subjectRouter = require("./subject/subject.route")
const classSectionRouter = require("./class_section/class_section.route")
const lessonRouter = require("./lesson/lesson.route")

router.use("/departments", departmentRouter);
router.use("/academic-years", academicYearRouter);
router.use("/semesters", semesterRouter);
router.use("/subjects", subjectRouter);
router.use("/class-sections", classSectionRouter);
router.use("/lessons", lessonRouter);
module.exports = router;