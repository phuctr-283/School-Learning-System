const express = require("express");
const router = express.Router();

const dashboardController = require("../../../controllers/school_admin/dashboard.controller");

router.get("/", dashboardController.showIndexPage);
router.get("/university", dashboardController.showUniversityPage);

module.exports = router;