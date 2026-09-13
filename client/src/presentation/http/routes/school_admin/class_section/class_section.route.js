const express = require("express");
const router = express.Router();

const classSectionController = require("../../../controllers/school_admin/class_section.controller");

router.get("/", classSectionController.list.bind(classSectionController));

module.exports = router;
