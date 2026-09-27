const {
  getStudentAssignmentUseCase,
  saveStudentAssignmentUseCase,
  submitStudentAssignmentUseCase,
} = require("../../../../infrastructure/dependencies/assignment/student_assignment_dependency");
const {getStudentAssignmentApplicationUseCase} = require("../../../../infrastructure/dependencies/assignment/assignment_dependency");
class AssignmentController {
  async takeAssignment(req, res) {
    const access = req.session?.assignmentAccess;
    if (!access) {
      return res.status(403).render("errors/403", {
        title: "Không có quyền truy cập",
        message: "Phiên truy cập bài tập không tồn tại hoặc đã hết hạn.",
        blank: true,
      });
    }
    const assignmentApplicationId = String(
      req.params.assignmentApplicationId || "",
    ).trim();
    if (
      !assignmentApplicationId ||
      assignmentApplicationId !== String(access.assignmentApplicationId)
    ) {
      return res.status(403).render("errors/403", {
        title: "Không được phép truy cập",
        message: "Bài tập không thuộc phiên truy cập hiện tại.",
        blank: true,
      });
    }
    try {
      const assignment = await getStudentAssignmentUseCase.execute({
        studentId: access.studentId,
        assignmentApplicationId: access.assignmentApplicationId,
        classSectionId: access.classSectionId,
        lessonId: access.lessonId,
      });
      const deadlineAt = Date.parse(assignment.deadline_at);
      if (!Number.isFinite(deadlineAt)) {
        throw new Error("Dữ liệu deadline của bài tập không hợp lệ.");
      }
      req.session.assignmentAccess = {
        ...access,
        mode: "taking",
        attemptId: assignment.attempt_id,
        attemptDeadlineAt: deadlineAt,
        expiresAt: deadlineAt + 10_000,
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
      const savedAnswersJson = JSON.stringify(assignment.saved_answers || {});
      return res.render("student/assignment/take-assignment", {
        title: assignment.title,
        assignment,
        assignmentApplicationId: assignment.assignment_application_id,
        attemptId: assignment.attempt_id,
        remainingSeconds: assignment.remaining_seconds,
        savedAnswersJson,
        blank: true,
        backUrl: "/student/assignment/qr",
      });
    } catch (error) {
      return this.renderError(res, error, "Không thể tải bài tập.");
    }
  }

  async saveAssignment(req, res) {
    const access = req.session?.assignmentAccess;
    if (!access || access.mode !== "taking") {
      return res.status(403).json({
        success: false,
        message: "Phiên làm bài không tồn tại hoặc đã hết hạn.",
      });
    }
    const attemptId = String(req.body.attempt_id || "").trim();
    if (!attemptId || attemptId !== String(access.attemptId)) {
      return res.status(403).json({
        success: false,
        message: "Lượt làm bài không hợp lệ.",
      });
    }
    try {
      const result = await saveStudentAssignmentUseCase.execute({
        studentId: access.studentId,
        assignmentApplicationId: access.assignmentApplicationId,
        classSectionId: access.classSectionId,
        lessonId: access.lessonId,
        attemptId,
        answers: req.body.answers || {},
      });
      if (result?.deadline_at) {
        const deadlineAt = Date.parse(result.deadline_at);

        if (Number.isFinite(deadlineAt)) {
          req.session.assignmentAccess.attemptDeadlineAt = deadlineAt;
          req.session.assignmentAccess.expiresAt = deadlineAt + 10_000;
        }
      }
      return res.json({
        success: true,
        data: result,
      });
    } catch (error) {
      const status = error.status || 500;

      return res.status(status).json({
        success: false,
        message: error.message || "Không thể lưu bài.",
      });
    }
  }

  async submitAssignment(req, res) {
    const access = req.session?.assignmentAccess;
    if (!access || access.mode !== "taking") {
      return res.status(403).json({
        success: false,
        message: "Phiên làm bài không tồn tại hoặc đã hết hạn.",
      });
    }
    const attemptId = String(req.body.attempt_id || "").trim();
    if (!attemptId || attemptId !== String(access.attemptId)) {
      return res.status(403).json({
        success: false,
        message: "Lượt làm bài không hợp lệ.",
      });
    }
    try {
      const result = await submitStudentAssignmentUseCase.execute({
        studentId: access.studentId,
        assignmentApplicationId: access.assignmentApplicationId,
        classSectionId: access.classSectionId,
        lessonId: access.lessonId,
        attemptId,
        answers: req.body.answers || {},
      });
      req.session.assignmentAccess = {
        ...access,
        mode: "completed",
        attemptId,
        expiresAt: Date.now() + 60_000,
      };
      return res.json({
        success: true,
        data: result,
      });
    } catch (error) {
      const status = error.status || 500;

      return res.status(status).json({
        success: false,
        message: error.message || "Không thể nộp bài.",
      });
    }
  }
  renderError(res, error, fallbackMessage) {
    const status = error.status || error.response?.status || 500;

    const message = error.message || fallbackMessage;

    if (status === 400) {
      return res.status(400).render("errors/400", {
        title: "Yêu cầu không hợp lệ",
        message,
        blank: true,
      });
    }

    if (status === 403) {
      return res.status(403).render("errors/403", {
        title: "Không được phép truy cập",
        message,
        blank: true,
      });
    }

    if (status === 404) {
      return res.status(404).render("errors/404", {
        title: "Không tìm thấy",
        message,
        blank: true,
      });
    }

    if (status === 409) {
      return res.status(409).render("student/assignment/locked", {
        title: "Bài tập đã khóa",
        message,
        blank: true,
      });
    }

    return res.status(500).render("errors/500", {
      title: "Lỗi máy chủ",
      message: fallbackMessage,
      blank: true,
    });
  }
  async getAssignmentApplications(req, res, next) {
    try {
      const classSectionId = String(req.params.classSectionId ?? "").trim();

      const lessonId = String(req.params.lessonId ?? "").trim();

      if (!classSectionId) {
        throw new Error("Thiếu mã lớp học phần.");
      }

      if (!lessonId) {
        throw new Error("Thiếu mã bài học.");
      }

      const assignments = await getStudentAssignmentApplicationUseCase.execute({
        req,
        classSectionId,
        lessonId,
      });

      const subjectName = assignments[0]?.subjectName ?? "";

      return res.render("student/assignment/assignment", {
        assignments,
        subjectName,
        classSectionId,
        lessonId,
      });
    } catch (error) {
      const errorStatus =
        Number(error.status) || Number(error.response?.status) || 500;

      const message = error.message || "Không thể tải danh sách bài tập.";

      return res.status(errorStatus).render(`errors/${errorStatus}`, {
        title: "Không thể tải dữ liệu",
        message,
        blank: true,
      });
    }
  }
}

module.exports = new AssignmentController();
