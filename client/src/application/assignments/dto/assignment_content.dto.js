class AssignmentContentDTO {
  constructor({
    assignment_id,
    university_id,
    subject_id,
    subject_name,
    teacher_id,
    title,
    description,
    assignment_type,
    total_score,
    duration_minutes,
    status,
    is_active,
    created_at,
    updated_at,
  }) {
    this.assignment_id = assignment_id;
    this.university_id = university_id;
    this.subject_id = subject_id;
    this.subject_name = subject_name;
    this.teacher_id = teacher_id;
    this.title = title;
    this.description = description ?? null;
    this.assignment_type = assignment_type;
    this.total_score = total_score;
    this.duration_minutes = duration_minutes;
    this.status = status;
    this.is_active = is_active;
    this.created_at = created_at;
    this.updated_at = updated_at;
  }
  static fromResponse(data) {
    return new AssignmentContentDTO(data);
  }

}

module.exports = AssignmentContentDTO;
