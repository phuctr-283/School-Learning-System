const AccountLevel = require("../../../domain/enums/account_level");

function userMiddleware(req, res, next) {
  const user = req.session?.user || null;
  res.locals.user = user;
  res.locals.accountLevel = user?.account_level ?? null;
  res.locals.isAuthenticated = Boolean(user);
  res.locals.isSuperAdmin = user?.account_level === AccountLevel.SUPER_ADMIN;
  res.locals.isSchoolAdmin = user?.account_level === AccountLevel.SCHOOL_ADMIN;
  res.locals.isTeacher = user?.account_level === AccountLevel.TEACHER;
  res.locals.isStudent = user?.account_level === AccountLevel.STUDENT;
  next();
}

module.exports = userMiddleware;
