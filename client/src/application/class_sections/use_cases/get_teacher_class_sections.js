class GetTeacherClassSectionsUseCase {
  constructor(classSectionRepository) {
    this.classSectionRepository = classSectionRepository;
  }

  async execute(req, subjectId) {
    return await this.classSectionRepository.getTeacherClassSections(
      req,
      subjectId,
    );
  }
}

module.exports = GetTeacherClassSectionsUseCase;
