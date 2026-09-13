const express = require("express");
const router = express.Router();
const multer = require("multer");

const upload = multer({dest: "uploads/",limits: {fileSize: 128 * 1024 * 1024,},});

const classSectionController = require("../../../controllers/school_admin/class_section.controller");


router.get("/import", classSectionController.importClassSectionPage.bind(classSectionController));
router.post("/import",upload.single("file"),classSectionController.importClassSections.bind(classSectionController));
module.exports = router;
