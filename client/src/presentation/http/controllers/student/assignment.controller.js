const {
  verifyStudentAssignmentQrUseCase,
} = require("../../../../infrastructure/dependencies/assignment/assignment_dependency");
const {
  getStudentAssignmentUseCase,
  saveStudentAssignmentUseCase,
  submitStudentAssignmentUseCase,
} = require("../../../../infrastructure/dependencies/assignment/student_assignment_dependency");
class AssignmentController {
  async assignmentQrEntry(req, res) {
    try {
      const qrCode = String(req.query["QR-CODE"] || "").toUpperCase();

      if (qrCode !== "TRUE") {
        return res.status(400).render("errors/400", {
          title: "QR không hợp lệ",
          message: "Mã QR không hợp lệ.",
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
          message: "Mã QR không chứa đủ dữ liệu.",
        });
      }

      return res.render("student/assignment/qr_student_code", {
        title: "Nhập mã sinh viên",

        assignmentApplicationId,

        classSectionId,

        lessonId,
        blank: true,
      });
    } catch (error) {
      console.error("ASSIGNMENT QR ENTRY ERROR:", error);
      return res.status(500).render("student/assignment/qr_student_code", {
        title: "Nhập mã sinh viên",

        assignmentApplicationId,

        classSectionId,

        lessonId,
        blank: true,
      });
    }
  }
  async verifyStudentAssignmentQr(req, res) {
    try {
      const studentId = String(req.body.student_id || "").trim();

      const assignmentApplicationId = String(
        req.body.assignment_application_id || "",
      ).trim();

      const classSectionId = String(req.body.class_section_id || "").trim();

      const lessonId = String(req.body.lesson_id || "").trim();

      const result = await verifyStudentAssignmentQrUseCase.execute(req, {
        studentId,
        assignmentApplicationId,
        classSectionId,
        lessonId,
      });

      // -----------------------------------------
      // Tạo quyền truy cập tạm thời
      // -----------------------------------------

      req.session.assignmentAccess = {
        assignmentApplicationId: result.assignment_application_id,

        classSectionId: result.class_section_id,

        lessonId: result.lesson_id,

        studentId: result.student_id,

        expiresAt: Date.now() + 5 * 60 * 1000,
      };

      return res.redirect(
        `/student/assignment/take/${encodeURIComponent(
          result.assignment_application_id,
        )}` +
          `?class_section_id=${encodeURIComponent(result.class_section_id)}` +
          `&lesson_id=${encodeURIComponent(result.lesson_id)}`,
      );
    } catch (error) {
      console.error("VERIFY STUDENT ASSIGNMENT QR ERROR:", error);

      return res.status(400).render("student/assignment/qr_student_code", {
        title: "Nhập mã sinh viên",

        assignmentApplicationId: req.body.assignment_application_id,

        classSectionId: req.body.class_section_id,

        lessonId: req.body.lesson_id,
        blank: true,
        error: error.message || "Không thể xác thực mã sinh viên.",
      });
    }
  }
  async takeAssignment(req, res) {
    try {
      const access = req.session?.assignmentAccess;

      if (!access) {
        return res.status(403).render("error", {
          message: "Phiên truy cập bài tập không hợp lệ.",
        });
      }

      const assignmentApplicationId = String(
        req.params.assignmentApplicationId || "",
      ).trim();

      if (assignmentApplicationId !== String(access.assignmentApplicationId)) {
        return res.status(403).render("error", {
          message: "Bài tập không hợp lệ.",
        });
      }

      const assignment = await getStudentAssignmentUseCase.execute(req, {
        studentId: access.studentId,
        assignmentApplicationId,
        classSectionId: access.classSectionId,
        lessonId: access.lessonId,
      });

      console.log("ASSIGNMENT DATA:", JSON.stringify(assignment, null, 2));

      return res.render("student/assignment/take-assignment", {
        title: assignment.title,
        assignment,
        assignmentApplicationId,
        attemptId: assignment.attempt_id,
        remainingSeconds: assignment.remaining_seconds,
        savedAnswersJson: JSON.stringify(assignment.saved_answers || {}),
        classSectionId: access.classSectionId,
        lessonId: access.lessonId,
        blank: true,
        backUrl: `/student/class-section/${access.classSectionId}`,
      });
    } catch (error) {
      console.error("TAKE ASSIGNMENT ERROR:", error);

      const message = error.message || "Không thể tải bài tập.";

      if (message === "Bài tập này đã được nộp và không thể làm lại.") {
        return res.status(403).render("student/assignment/assignment-locked", {
          title: "Không thể làm bài",
          message,
        });
      }

      return res.status(500).render("error", {
        message,
      });
    }
  }

  async saveAssignment(req, res) {
    try {
      const access = req.session?.assignmentAccess;

      if (!access) {
        return res.status(403).json({
          success: false,
          message: "Phiên truy cập không hợp lệ.",
        });
      }

      const attemptId = String(req.body.attempt_id || "").trim();

      const result = await saveStudentAssignmentUseCase.execute(req, {
        studentId: access.studentId,

        assignmentApplicationId: access.assignmentApplicationId,

        classSectionId: access.classSectionId,

        lessonId: access.lessonId,

        attemptId,

        answers: req.body.answers || {},
      });

      return res.json({
        success: true,
        data: result,
      });
    } catch (error) {
      console.error("SAVE ASSIGNMENT ERROR:", error);

      return res.status(400).json({
        success: false,
        message: error.message || "Không thể lưu bài làm.",
      });
    }
  }

  async submitAssignment(req, res) {
    try {
      const access = req.session?.assignmentAccess;

      if (!access) {
        return res.status(403).json({
          success: false,
          message: "Phiên truy cập không hợp lệ.",
        });
      }

      const attemptId = String(req.body.attempt_id || "").trim();

      const result = await submitStudentAssignmentUseCase.execute(req, {
        studentId: access.studentId,

        assignmentApplicationId: access.assignmentApplicationId,

        classSectionId: access.classSectionId,

        lessonId: access.lessonId,

        attemptId,

        answers: req.body.answers || {},
      });

      return res.json({
        success: true,
        data: result,
      });
    } catch (error) {
      console.error("SUBMIT ASSIGNMENT ERROR:", error);

      return res.status(400).json({
        success: false,
        message: error.message || "Không thể nộp bài.",
      });
    }
  }
}

module.exports = new AssignmentController();
