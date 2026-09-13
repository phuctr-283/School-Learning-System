const CreateSubjectLessonPlanDTO = require(
  "../dto/create_subject_lesson_plan.dto"
);

class CreateSubjectLessonPlanUseCase {
  constructor(subjectLessonPlanRepository) {
    this.subjectLessonPlanRepository = subjectLessonPlanRepository;
  }

  async execute(req, data) {
    const dto = CreateSubjectLessonPlanDTO.fromRequestBody(data);

    return await this.subjectLessonPlanRepository.createSubjectLessonPlan(
      req,
      dto,
    );
  }
}

module.exports = CreateSubjectLessonPlanUseCase;