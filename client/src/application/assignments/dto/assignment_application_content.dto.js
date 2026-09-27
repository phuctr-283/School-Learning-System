class AssignmentApplicationContentDTO {
  constructor(data = {}) {
    this.assignmentApplicationId = data.assignment_application_id ?? "";
    this.assignmentId = data.assignment_id ?? "";
    this.universityId = data.university_id ?? "";
    this.lessonId = data.lesson_id ?? "";
    this.classSectionId = data.class_section_id ?? "";
    this.classSectionStatus = data.class_section_status ?? "";
    this.classSectionOpenedAt = data.class_section_opened_at ?? null;
    this.classSectionClosedAt = data.class_section_closed_at ?? null;
    this.title = data.title ?? "";
    this.description = data.description ?? null;
    this.subjectId = data.subject_id ?? "";
    this.subjectName = data.subject_name ?? "";
    this.assignmentType = data.assignment_type ?? "";
    this.totalScore = data.total_score ?? 0;
    this.durationMinutes = data.duration_minutes ?? 0;
    this.status = data.status ?? "";
    this.maxAttempts = data.max_attempts ?? 1;
    this.openAt = data.open_at ?? null;
    this.dueAt = data.due_at ?? null;
    this.createdAt = data.created_at ?? null;
    this.updatedAt = data.updated_at ?? null;
  }
}

module.exports = AssignmentApplicationContentDTO;
