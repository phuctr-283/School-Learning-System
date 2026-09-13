class GetActiveAndPlannedAcademicYearsUseCase {

  constructor(academicYearRepository) {
    this.academicYearRepository =
      academicYearRepository;
  }

  async execute(req) {

    return await this.academicYearRepository
      .getActiveAndPlannedAcademicYears(req);

  }

}

module.exports =
  GetActiveAndPlannedAcademicYearsUseCase;