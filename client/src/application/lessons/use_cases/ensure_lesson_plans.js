class EnsureLessonPlansUseCase {

  constructor(
    lessonPlanRepository,
  ) {

    this.lessonPlanRepository =
      lessonPlanRepository;
  }


  async execute(
    req,
    config = {},
  ) {

    return await this.lessonPlanRepository
      .ensureLessonPlans(
        req,
        config,
      );
  }

}


module.exports =
  EnsureLessonPlansUseCase;