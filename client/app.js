require("dotenv").config();

const express = require("express");
const session = require("express-session");
const path = require("path");
const cookieParser = require("cookie-parser");
const logger = require("morgan");
const { engine } = require("express-handlebars");
const helpers = require("./src/presentation/http/helpers/index")

// =========================================================
// APP
// =========================================================

const app = express();

// =========================================================
// PATHS
// =========================================================

const viewsPath = path.join(__dirname, "src", "presentation", "views");
const publicPath = path.join(__dirname, "public");

// =========================================================
// HANDLEBARS
// =========================================================

app.engine(
  "hbs",
  engine({
    extname: ".hbs",
    defaultLayout: "main",
    layoutsDir: path.join(viewsPath, "layouts"),
    partialsDir: path.join(viewsPath, "partials"),
    helpers,
  }),
);

app.set("views", viewsPath);
app.set("view engine", "hbs");

// =========================================================
// SYSTEM MIDDLEWARE
// =========================================================

app.use(logger("dev"));
app.use(express.json());
app.use(
  express.urlencoded({
    extended: true,
  }),
);

app.use(cookieParser());

// =====================================================
// SESSION
// =====================================================

app.use(
    session({
        secret: process.env.SESSION_SECRET || "school-system-secret",
        resave: false,
        saveUninitialized: false,

        cookie: {
            secure: false,
            httpOnly: true,
            maxAge: 1000 * 60 * 60 * 24
        }
    })
);

const userMiddleware = require("./src/presentation/http/middlewares/user.middleware")
app.use(userMiddleware);
// =========================================================
// STATIC
// =========================================================

app.use(express.static(publicPath));

// =========================================================
// ROUTES
// =========================================================

const authenticationRouter = require("./src/presentation/http/routes/auth.route");
const superAdminRouter = require("./src/presentation/http/routes/super_admin.route")
const schoolAdminRouter = require("./src/presentation/http/routes/school_admin.route")
const teacherRouter = require("./src/presentation/http/routes/teacher.route")

app.use("/", authenticationRouter);
app.use("/super-admin", superAdminRouter);
app.use("/school-admin", schoolAdminRouter);
app.use("/teacher", teacherRouter);

// =========================================================
// 404
// =========================================================

app.use((req, res, next) => {
  const error = new Error("Không tìm thấy trang");
  error.status = 404;
  next(error);
});

// =========================================================
// GLOBAL ERROR HANDLER
// =========================================================

app.use((err, req, res, next) => {
  const statusCode = err.status || 500;
  res.status(statusCode);
  res.render("error", {
    layout: false,
    message: err.message || "Đã xảy ra lỗi",
    error: process.env.NODE_ENV === "development" ? err : {},
  });
});

// =========================================================
// EXPORT
// =========================================================

module.exports = app;
