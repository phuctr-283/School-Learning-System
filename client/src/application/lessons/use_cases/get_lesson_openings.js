class GetLessonOpeningsUseCase {

  constructor(
    lessonOpeningRepository
  ) {

    this.lessonOpeningRepository =
      lessonOpeningRepository;
  }


  async execute(
    req,
    classSectionLessonPlanId
  ) {

    if (!classSectionLessonPlanId) {

      throw new Error(
        "Thiếu mã kế hoạch lớp học phần."
      );
    }


    return await this.lessonOpeningRepository
      .getLessonOpenings(
        req,
        classSectionLessonPlanId
      );
  }

}


module.exports =
  GetLessonOpeningsUseCase;