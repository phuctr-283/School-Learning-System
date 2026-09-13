class EnsureLessonOpeningsUseCase {

  constructor(
    lessonOpeningRepository
  ) {

    this.lessonOpeningRepository =
      lessonOpeningRepository;
  }


  async execute(
    req
  ) {

    return await this.lessonOpeningRepository
      .ensureLessonOpenings(
        req
      );
  }

}


module.exports =
  EnsureLessonOpeningsUseCase;