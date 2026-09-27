function assignmentQrAccessMiddleware(req, res, next) {
  const access = req.session?.assignmentAccess;

  if (!access) {
    return res.status(403).render("errors/403", {
      title: "Không có quyền truy cập",
      message: "Phiên truy cập bài tập không tồn tại hoặc đã hết hạn.",
      blank: true,
    });
  }

  const routeApplicationId = String(
    req.params.assignmentApplicationId || "",
  ).trim();

  if (routeApplicationId !== String(access.assignmentApplicationId)) {
    return res.status(403).render("errors/403", {
      title: "Không được phép truy cập",
      message: "Bài tập không thuộc phiên hiện tại.",
      blank: true,
    });
  }

  if (
    !access.assignmentApplicationId ||
    !access.classSectionId ||
    !access.lessonId ||
    !access.studentId
  ) {
    delete req.session.assignmentAccess;

    return res.status(403).render("errors/403", {
      title: "Phiên truy cập không hợp lệ",
      message: "Thông tin truy cập bài tập không đầy đủ.",
      blank: true,
    });
  }
  if (access.mode === "verified") {
    if (!access.expiresAt || Date.now() > Number(access.expiresAt)) {
      delete req.session.assignmentAccess;
      return res.status(403).render("errors/403", {
        title: "Phiên QR đã hết hạn",
        message: "Vui lòng quét QR và xác thực lại.",
        blank: true,
      });
    }
    return next();
  }
  if (access.mode === "taking") {
    if (!access.attemptId) {
      delete req.session.assignmentAccess;

      return res.status(403).render("errors/403", {
        title: "Phiên làm bài không hợp lệ",
        message: "Không tìm thấy lượt làm bài.",
        blank: true,
      });
    }
    return next();
  }

  return res.status(403).render("errors/403", {
    title: "Không được phép truy cập",
    message: "Phiên truy cập bài tập không hợp lệ.",
    blank: true,
  });
}

module.exports = assignmentQrAccessMiddleware;
