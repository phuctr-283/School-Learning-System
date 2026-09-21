class AssignmentListDTO {
  constructor({
    assignment_id,
    subject_name,
    title,
    description = null,
    assignment_type,
    total_score,
    status,
    is_active,
    created_at,
  }) {
    this.assignmentId = String(assignment_id || "");
    this.subjectName = String(subject_name || "");

    this.title = String(title || "");

    this.description = typeof description === "string" ? description : null;

    this.assignmentType = String(assignment_type || "");

    this.totalScore = total_score;

    this.status = String(status || "");

    this.isActive = Boolean(is_active);

    this.createdAt = created_at;
  }

  static fromResponse(data = {}) {
    return new AssignmentListDTO(data);
  }
}

module.exports = AssignmentListDTO;
