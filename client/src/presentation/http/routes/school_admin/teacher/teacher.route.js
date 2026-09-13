const express = require("express");

const router = express.Router();

const TeacherController = require(
  "../../../controllers/school_admin/teacher.controller",
);


// =========================================
// GET TEACHERS
// =========================================

router.get(
  "/",
  TeacherController.list.bind(
    TeacherController,
  ),
);


module.exports =
  router;