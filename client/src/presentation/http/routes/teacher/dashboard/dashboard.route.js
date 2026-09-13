const express = require("express");
const router = express.Router();

const dashboardController = require("../../../controllers/teacher/dashboard.controller")

router.get("/", dashboardController.showIndexPage.bind(dashboardController));
module.exports = router;
