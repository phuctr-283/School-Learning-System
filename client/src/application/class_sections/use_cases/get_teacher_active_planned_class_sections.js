class GetTeacherActivePlannedClassSectionsUseCase {
  constructor(classSectionRepository) {
    this.classSectionRepository = classSectionRepository;
  }

  async execute(req, { subjectId, academicYearId, semesterId }) {
    if (!subjectId) {
      throw new Error("Thiếu mã môn học.");
    }

    if (!academicYearId) {
      throw new Error("Thiếu mã năm học.");
    }

    if (!semesterId) {
      throw new Error("Thiếu mã học kỳ.");
    }

    return this.classSectionRepository.getTeacherActivePlannedClassSections(
      req,
      subjectId,
      academicYearId,
      semesterId,
    );
  }
}

module.exports = GetTeacherActivePlannedClassSectionsUseCase;
