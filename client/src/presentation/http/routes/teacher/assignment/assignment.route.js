const express = require("express");
const router = express.Router();

const subjectRouter = require("../subject/subject.route");
const classSectionRouter = require("../class_section/class_section.route");

router.use("/", subjectRouter);
router.use("/", classSectionRouter);
module.exports = router;    