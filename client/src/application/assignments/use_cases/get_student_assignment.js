class GetStudentAssignmentUseCase {

  constructor(repository) {
    this.repository = repository;
  }


  async execute(
    req,
    params
  ) {

    if (!params.studentId) {
      throw new Error(
        "Không xác định được sinh viên."
      );
    }

    if (!params.assignmentApplicationId) {
      throw new Error(
        "Thiếu mã bài tập."
      );
    }

    if (!params.classSectionId) {
      throw new Error(
        "Thiếu mã lớp học phần."
      );
    }

    if (!params.lessonId) {
      throw new Error(
        "Thiếu mã bài học."
      );
    }

    return this.repository.getStudentAssignment(
      req,
      {
        student_id: params.studentId,
        assignment_application_id:
          params.assignmentApplicationId,
        class_section_id:
          params.classSectionId,
        lesson_id:
          params.lessonId,
      }
    );
  }

}

module.exports =
  GetStudentAssignmentUseCase;