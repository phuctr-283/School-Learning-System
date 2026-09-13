class GetTeacherSubjectsUseCase {

  constructor(
    classSectionRepository,
  ) {

    this.classSectionRepository =
      classSectionRepository;
  }


  async execute(req) {

    return await this
      .classSectionRepository
      .getTeacherSubjects(req);
  }

}


module.exports =
  GetTeacherSubjectsUseCase;