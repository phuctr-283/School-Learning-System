class GetTeacherActivePlannedSubjectsUseCase {
  constructor(classSectionRepository) {
    this.classSectionRepository = classSectionRepository;
  }

  async execute(req, { academicYearId, semesterId }) {
    if (!academicYearId) {
      throw new Error("Thiếu mã năm học.");
    }

    if (!semesterId) {
      throw new Error("Thiếu mã học kỳ.");
    }

    return this.classSectionRepository.getTeacherActivePlannedSubjects(
      req,
      academicYearId,
      semesterId,
    );
  }
}

module.exports = GetTeacherActivePlannedSubjectsUseCase;
