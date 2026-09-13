class GetAcademicYearsUseCase {

  constructor(
    academicYearRepository
  ) {

    this.academicYearRepository =
      academicYearRepository;
  }


  async execute(req) {

    return await this.academicYearRepository
      .getAcademicYears(req);
  }

}

module.exports = GetAcademicYearsUseCase;