const {
  verifyStudentAssignmentQrUseCase,
} = require("../../../../infrastructure/dependencies/assignment/assignment_dependency");

class AssignmentQrController {
  async assignmentQrEntry(req, res) {
    const qrCode = String(req.query["QR-CODE"] || "")
      .trim()
      .toUpperCase();
    if (qrCode !== "TRUE") {
      return res.status(400).render("errors/400", {
        title: "Yêu cầu không hợp lệ",
        message: "Đường dẫn QR không hợp lệ.",
        blank: true,
      });
    }
    const assignmentApplicationId = String(
      req.query.assignment_application_id || "",
    ).trim();
    const classSectionId = String(req.query.class_section_id || "").trim();
    const lessonId = String(req.query.lesson_id || "").trim();

    if (!assignmentApplicationId || !classSectionId || !lessonId) {
      return res.status(400).render("errors/400", {
        title: "QR không hợp lệ",
        message: "Mã QR không chứa đủ dữ liệu bài tập.",
        blank: true,
      });
    }

    return res.render("student/assignment/qr_student_code", {
      title: "Xác thực bài tập",
      assignmentApplicationId,
      classSectionId,
      lessonId,
      blank: true,
    });
  }
  async verifyStudentAssignmentQr(req, res) {
    const studentId = String(req.body.student_id || "").trim();
    const assignmentApplicationId = String(
      req.body.assignment_application_id || "",
    ).trim();
    const classSectionId = String(req.body.class_section_id || "").trim();
    const lessonId = String(req.body.lesson_id || "").trim();
    if (
      !studentId ||
      !assignmentApplicationId ||
      !classSectionId ||
      !lessonId
    ) {
      return res.status(400).render("errors/400", {
        title: "Thông tin không hợp lệ",
        message: "Vui lòng nhập đầy đủ thông tin.",
        blank: true,
      });
    }
    try {
      await verifyStudentAssignmentQrUseCase.execute({
        studentId,
        assignmentApplicationId,
        classSectionId,
        lessonId,
      });
      const now = Date.now();
      req.session.assignmentAccess = {
        mode: "verified",
        assignmentApplicationId,
        classSectionId,
        lessonId,
        studentId,
        qrVerifiedAt: now,
        expiresAt: now + 5 * 60 * 1000,
        attemptId: null,
        attemptDeadlineAt: null,
      };
      await new Promise((resolve, reject) => {
        req.session.save((error) => {
          if (error) {
            reject(error);
            return;
          }
          resolve();
        });
      });
      return res.redirect(
        `/student/assignment/take/${encodeURIComponent(assignmentApplicationId)}`,
      );
    } catch (error) {
      const errorStatus =
        Number(error.status) || Number(error.response?.status) || 500;

      const message = error.message || "Không thể xác thực QR.";

      if (errorStatus === 400) {
        return res.status(400).render("errors/400", {
          title: "Thông tin không hợp lệ",
          message,
          blank: true,
        });
      }

      if (errorStatus === 403) {
        return res.status(403).render("errors/403", {
          title: "Không được phép truy cập",
          message,
          blank: true,
        });
      }

      if (errorStatus === 404) {
        return res.status(404).render("errors/404", {
          title: "Không tìm thấy bài tập",
          message,
          blank: true,
        });
      }

      if (errorStatus === 409) {
        return res.status(409).render("student/assignment/locked", {
          title: "Bài tập chưa khả dụng",
          message,
          blank: true,
        });
      }

      return res.status(500).render("errors/500", {
        title: "Lỗi máy chủ",
        message: "Không thể xác thực QR.",
        blank: true,
      });
    }
  }
}

module.exports = new AssignmentQrController();
