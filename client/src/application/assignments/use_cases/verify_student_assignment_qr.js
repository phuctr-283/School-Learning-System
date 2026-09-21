class VerifyStudentAssignmentQrUseCase {
  constructor(repository) {
    this.repository = repository;
  }

  async execute(req, payload) {
    const studentId = String(payload.studentId || "").trim();

    const assignmentApplicationId = String(
      payload.assignmentApplicationId || "",
    ).trim();

    const classSectionId = String(payload.classSectionId || "").trim();

    const lessonId = String(payload.lessonId || "").trim();

    if (!studentId) {
      throw new Error("Vui lòng nhập mã sinh viên.");
    }

    if (!assignmentApplicationId) {
      throw new Error("Thiếu mã bài tập.");
    }

    if (!classSectionId) {
      throw new Error("Thiếu mã lớp học phần.");
    }

    if (!lessonId) {
      throw new Error("Thiếu mã bài học.");
    }

    return this.repository.verifyStudentAssignmentQr(req, {
      student_id: studentId,
      assignment_application_id: assignmentApplicationId,
      class_section_id: classSectionId,
      lesson_id: lessonId,
    });
  }
}

module.exports = VerifyStudentAssignmentQrUseCase;
