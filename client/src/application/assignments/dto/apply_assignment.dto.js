class ApplyAssignmentDTO {
  constructor({ assignmentId, lessonId, classSectionIds, maxAttempts = 1 }) {
    this.assignmentId = assignmentId;
    this.lessonId = lessonId;

    this.classSectionIds = Array.isArray(classSectionIds)
      ? [
          ...new Set(
            classSectionIds.map((id) => String(id).trim()).filter(Boolean),
          ),
        ]
      : [];

    this.maxAttempts = Number(maxAttempts);
  }

  validate() {
    if (!this.assignmentId) {
      throw new Error("Thiếu mã bài tập.");
    }

    if (!this.lessonId) {
      throw new Error("Thiếu mã buổi học.");
    }

    if (
      !Array.isArray(this.classSectionIds) ||
      this.classSectionIds.length === 0
    ) {
      throw new Error("Phải chọn ít nhất một nhóm lớp học phần.");
    }

    if (!Number.isInteger(this.maxAttempts) || this.maxAttempts < 1) {
      throw new Error("Số lần làm bài phải lớn hơn hoặc bằng 1.");
    }

    return this;
  }

  toRequestBody() {
    this.validate();

    return {
      assignment_id: this.assignmentId,

      lesson_id: this.lessonId,

      class_section_ids: this.classSectionIds,

      max_attempts: this.maxAttempts,
    };
  }

  static fromRequest(input = {}) {
    return new ApplyAssignmentDTO({
      assignmentId: input.assignmentId ?? input.assignment_id,

      lessonId: input.lessonId ?? input.lesson_id,

      classSectionIds: input.classSectionIds ?? input.class_section_ids,

      maxAttempts: input.maxAttempts ?? input.max_attempts ?? 1,
    });
  }
}

module.exports = ApplyAssignmentDTO;
