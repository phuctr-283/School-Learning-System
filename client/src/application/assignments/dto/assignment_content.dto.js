class AssignmentDTO {
  constructor(data = {}) {
    this.assignmentId = data.assignment_id ?? null;

    this.title = data.title ?? "";

    this.description = data.description ?? null;

    this.universityId = data.university_id ?? null;

    this.departmentId = data.department_id ?? null;

    this.subjectId = data.subject_id ?? null;

    this.teacherId = data.teacher_id ?? null;

    this.totalScore = data.total_score ?? "0.00";

    this.assignmentType = data.assignment_type ?? "";

    this.status = data.status ?? "";

    this.isActive = data.is_active ?? false;

    this.createdAt = data.created_at ?? null;

    this.updatedAt = data.updated_at ?? null;
  }
}

module.exports = AssignmentDTO;
