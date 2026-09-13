class EnsureLessonPlansDTO {
  constructor({
    class_section_ids = [],
  } = {}) {
    this.classSectionIds = class_section_ids;
  }
}

module.exports = EnsureLessonPlansDTO;