const express = require("express");
const router = express.Router();

const AdministratorController = require("../../controllers/super_admin/administrator/administrator.controller");
const SuperAdminController = require("../../controllers/super_admin/administrator/super_admin.controller");
const SchoolAdminController = require("../../controllers/super_admin/administrator/school_admin.controller");

router.get("/school-admin/", SchoolAdminController.list.bind(SchoolAdminController));

router.post("/admin/register",AdministratorController.register.bind(AdministratorController),);

module.exports = router;
