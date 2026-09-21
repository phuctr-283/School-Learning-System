class LessonOpeningContentDTO {
  constructor({
    lesson_id,
    lesson_number,
    lesson_name,
    status,
    opened_at,
    closed_at,
  }) {
    this.lessonId = lesson_id ?? "";
    this.lessonNumber = lesson_number ?? 0;
    this.lessonName = lesson_name ?? "";
    this.status = status ?? "locked";
    this.openedAt = opened_at ?? null;
    this.closedAt = closed_at ?? null;
  }

  static fromResponse(data) {
    return new LessonOpeningContentDTO(data || {});
  }
}

module.exports = LessonOpeningContentDTO;