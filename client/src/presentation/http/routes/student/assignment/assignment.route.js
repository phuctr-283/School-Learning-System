const express = require("express");
const router = express.Router();

const classSectionRouter = require("../class_section/class_section.route");

router.use("/", classSectionRouter);
module.exports = router;
