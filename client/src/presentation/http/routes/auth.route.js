const express = require("express");
const router = express.Router();
const LoginController = require("../controllers/authentication/login.controller");

const LogoutController = require("../controllers/authentication/logout.controller");

const RegisterController = require("../controllers/authentication/register.controller");

const AdministratorController = require("../controllers/super_admin/administrator/administrator.controller");

const RefreshTokenController = require("../controllers/authentication/refresh_token.controller");

const verifyAssignmentRouter= require("./student/assignment/verify_assignment.route")

const guestMiddleware = require("../middlewares/guest.middleware");

router.get(
  "/",
  guestMiddleware,
  LoginController.showAuthentication.bind(LoginController),
);
router.post(
  "/login",
  guestMiddleware,
  LoginController.login.bind(LoginController),
);
router.post("/logout", LogoutController.logout.bind(LogoutController));
router.post(
  "/admin/register",
  AdministratorController.register.bind(AdministratorController),
);
router.post(
  "/refresh",
  RefreshTokenController.refresh.bind(RefreshTokenController),
);
router.get(
  "/register/departments",
  LoginController.getActiveDepartments.bind(LoginController),
);
router.post(
  "/register",
  guestMiddleware,
  RegisterController.register.bind(RegisterController),
);
router.use("/student", verifyAssignmentRouter);
module.exports = router;
