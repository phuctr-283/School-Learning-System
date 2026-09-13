const express = require("express");
const router = express.Router();

const SemesterController = require("../../../controllers/school_admin/semester.controller");

router.get("/", SemesterController.list.bind(SemesterController));
router.get("/create", SemesterController.showCreate.bind(SemesterController));
router.post("/create", SemesterController.create.bind(SemesterController));

module.exports = router;
