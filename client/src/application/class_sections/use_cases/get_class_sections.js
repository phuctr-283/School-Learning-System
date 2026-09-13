class GetClassSectionsUseCase {
  constructor(classSectionRepository) {
    this.classSectionRepository = classSectionRepository;
  }

  async execute(req) {
    return await this.classSectionRepository.getUniversityClassSections(req);
  }
}

module.exports = GetClassSectionsUseCase;
