const CreateSemesterLessonPlanDTO = require("../dto/create_semester_lesson_plan.dto");

class CreateSemesterLessonPlansUseCase {
  constructor(repository) {
    this.repository = repository;
  }

  async execute(req, data) {
    const dto =
      data instanceof CreateSemesterLessonPlanDTO
        ? data
        : CreateSemesterLessonPlanDTO.fromRequestBody(data);

    return await this.repository.createSemesterLessonPlans(req, dto);
  }
}

module.exports = CreateSemesterLessonPlansUseCase;
