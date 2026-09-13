const express = require("express");
const router = express.Router();

const universityRouter = require("./super_admin/university.route")
const administratorRouter = require("./super_admin/administrator.route")

const authMiddleware = require("../middlewares/auth.middleware");
const requireAccountLevel = require("../middlewares/require_account_level");
const AccountLevel = require("../../../domain/enums/account_level");


router.use(authMiddleware, requireAccountLevel(AccountLevel.SUPER_ADMIN));

router.get("/", (req, res) => {return res.render("super_admin/index", {title: "Dashboard",});});

router.use("/university", universityRouter);
router.use("/", administratorRouter);
module.exports = router;
