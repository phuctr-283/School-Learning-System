const express = require("express");
const router = express.Router();

const subjectController = require("../../../controllers/school_admin/subject.controller");

router.get("/", subjectController.list.bind(subjectController));
router.get("/create", subjectController.showCreate.bind(subjectController));
router.post("/create", subjectController.create.bind(subjectController));
module.exports = router;
