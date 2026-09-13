class LessonOpeningContentDTO {
  constructor({
    lesson_opening_id,
    university_id,
    university_name,
    class_section_lesson_plan_id,
    lesson_id,
    lesson_number,
    lesson_name,
    status,
    opened_at,
    closed_at,
    created_at,
    updated_at,
  }) {
    this.lessonOpeningId = lesson_opening_id;

    this.universityId = university_id;

    this.universityName = university_name;

    this.classSectionLessonPlanId = class_section_lesson_plan_id;

    this.lessonId = lesson_id;

    this.lessonNumber = lesson_number;

    this.lessonName = lesson_name;

    this.status = status;

    this.openedAt = opened_at;

    this.closedAt = closed_at;

    this.createdAt = created_at;

    this.updatedAt = updated_at;
  }

  static fromResponse(data) {
    return new LessonOpeningContentDTO(data);
  }
}

module.exports = LessonOpeningContentDTO;
