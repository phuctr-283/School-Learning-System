const express = require("express");

const router = express.Router();

const DepartmentController = require(
  "../../../controllers/school_admin/department.controller",
);


// =========================================
// GET DEPARTMENTS
// =========================================

router.get(
  "/",
  DepartmentController.list.bind(
    DepartmentController,
  ),
);


// =========================================
// CREATE PAGE
// =========================================

router.get(
  "/create",
  DepartmentController.showCreate.bind(
    DepartmentController,
  ),
);


// =========================================
// CREATE DEPARTMENT
// =========================================

router.post(
  "/create",
  DepartmentController.create.bind(
    DepartmentController,
  ),
);


module.exports = router;