function assignmentQrAccessMiddleware(req, res, next) {
  const access = req.session?.assignmentAccess;

  if (!access) {
    return res.redirect("/student/assignment/qr");
  }

  if (!access.expiresAt || Date.now() > access.expiresAt) {
    delete req.session.assignmentAccess;

    return res.status(403).render("errors/403", {
      title: "Phiên truy cập đã hết hạn",
    });
  }

  const applicationId = String(req.params.assignmentApplicationId || "");

  if (String(access.assignmentApplicationId) !== applicationId) {
    return res.status(403).render("errors/403", {
      title: "Không có quyền truy cập bài tập",
    });
  }

  return next();
}

module.exports = assignmentQrAccessMiddleware;
