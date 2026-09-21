class AssignmentApplicationDTO {
  constructor({
    assignment_application_id,
    assignment_id,
    class_section_ids,
    lesson_id,
    status,
    open_at,
    due_at,
    max_attempts,
  }) {
    this.assignmentApplicationId = assignment_application_id;

    this.assignmentId = assignment_id;

    this.classSectionIds = Array.isArray(class_section_ids)
      ? class_section_ids
      : [];

    this.lessonId = lesson_id;

    this.status = status;

    this.openAt = open_at ?? null;

    this.dueAt = due_at ?? null;

    this.maxAttempts = max_attempts;
  }
}

module.exports = AssignmentApplicationDTO;
