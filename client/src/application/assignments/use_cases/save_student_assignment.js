class SaveStudentAssignmentUseCase {

  constructor(repository) {
    this.repository = repository;
  }


  async execute(
    req,
    params
  ) {

    return this.repository.saveAnswers(
      req,
      {
        student_id: params.studentId,

        assignment_application_id:
          params.assignmentApplicationId,

        class_section_id:
          params.classSectionId,

        lesson_id:
          params.lessonId,

        attempt_id:
          params.attemptId,

        answers:
          params.answers || {},
      }
    );
  }

}

module.exports =
  SaveStudentAssignmentUseCase;