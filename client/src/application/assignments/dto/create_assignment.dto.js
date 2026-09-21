class CreateAssignmentDTO {
  constructor({
    subject_id,
    subjectId,

    title,
    description = null,

    assignment_type,
    assignmentType = "practice",

    duration_minutes,
    durationMinutes,

    questions = [],
  }) {
    this.subjectId = String(subject_id ?? subjectId ?? "").trim();

    this.title = String(title ?? "").trim();

    this.description =
      typeof description === "string" ? description.trim() || null : null;

    this.assignmentType = String(
      assignment_type ?? assignmentType ?? "practice",
    ).trim();

    const rawDuration = duration_minutes ?? durationMinutes;

    this.durationMinutes = Number(rawDuration);

    this.questions = Array.isArray(questions)
      ? questions.map((item) => {
          const normalized = {
            question_type: String(item?.question_type ?? "").trim(),

            question: String(item?.question ?? "").trim(),

            content: String(item?.content ?? ""),

            answer: String(item?.answer ?? ""),
          };

          if (
            item?.score !== undefined &&
            item?.score !== null &&
            item?.score !== ""
          ) {
            normalized.score = Number(item.score);
          }

          return normalized;
        })
      : [];
  }

  validate() {
    if (!this.title) {
      throw new Error("Tên bài tập không được để trống.");
    }

    if (!this.subjectId) {
      throw new Error("Chưa chọn môn học.");
    }

    if (!["practice", "homework", "quiz"].includes(this.assignmentType)) {
      throw new Error("Loại bài tập không hợp lệ.");
    }

    if (
      !Number.isInteger(this.durationMinutes) ||
      this.durationMinutes < 1 ||
      this.durationMinutes > 600
    ) {
      throw new Error("Thời gian làm bài phải từ 1 đến 600 phút.");
    }

    if (!Array.isArray(this.questions) || this.questions.length === 0) {
      throw new Error("Bài tập phải có ít nhất một câu hỏi.");
    }
  }

  toRequest() {
    this.validate();

    return {
      title: this.title,

      description: this.description,

      subject_id: this.subjectId,

      assignment_type: this.assignmentType,

      duration_minutes: this.durationMinutes,

      questions: this.questions,
    };
  }
}

module.exports = CreateAssignmentDTO;
