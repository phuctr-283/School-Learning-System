class ImportClassSectionsUseCase {
  constructor(classSectionRepository) {
    this.classSectionRepository = classSectionRepository;
  }

  async execute(req, file) {
    if (!file) {
      throw new Error("Vui lòng chọn file Excel.");
    }

    return await this.classSectionRepository.importClassSections(req, file);
  }
}

module.exports = ImportClassSectionsUseCase;
