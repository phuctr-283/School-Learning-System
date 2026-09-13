const express = require("express");
const router = express.Router({ mergeParams: true });
const universityController = require("../../controllers/super_admin/university.controller");

router.get("/", universityController.list);
router.get("/create", universityController.getCreateUniversityPage)
router.post("/create", universityController.createUniversity);

module.exports = router;
