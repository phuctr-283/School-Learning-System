class GetCourseLessonPlansUseCase {

  constructor(
    courseLessonPlanRepository,
  ) {

    this.courseLessonPlanRepository =
      courseLessonPlanRepository;
  }


  async execute(req) {

    return await this
      .courseLessonPlanRepository
      .getCourseLessonPlans(req);
  }
}


module.exports =
  GetCourseLessonPlansUseCase;