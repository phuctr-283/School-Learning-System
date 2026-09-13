class GetClassSectionLessonPlansUseCase {

  constructor(
    classSectionLessonPlanRepository,
  ) {
    this.classSectionLessonPlanRepository =
      classSectionLessonPlanRepository;
  }

  async execute(
    req,
    courseLessonPlanId,
  ) {

    if (!courseLessonPlanId) {
      throw new Error(
        "Course lesson plan ID không được để trống.",
      );
    }

    return await this
      .classSectionLessonPlanRepository
      .getClassSectionLessonPlans(
        req,
        courseLessonPlanId,
      );
  }
}

module.exports =
  GetClassSectionLessonPlansUseCase;