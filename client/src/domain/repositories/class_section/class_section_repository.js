class ClassSectionRepository {
  async getUniversityClassSections(req) {
    throw new Error("getUniversityClassSections() must be implemented");
  }

  async importClassSections(req, file) {
    throw new Error("importClassSections() must be implemented");
  }

  async getTeacherSubjects(req) {
    throw new Error("getTeacherSubjects() chưa được triển khai.");
  }

  async getTeacherActiveSubjects(req) {
    throw new Error("getTeacherActiveSubjects() chưa được triển khai.");
  }

  async getTeacherClassSections(req, subjectId) {
    throw new Error("getTeacherClassSections() chưa được triển khai.");
  }

  async getStudentClassSections(req) {
    throw new Error("getStudentSubjects() chưa được triển khai");
  }
  async getTeacherActivePlannedSubjects(req, academicYearId, semesterId) {
    throw new Error("getTeacherActiveSubjects() chưa được triển khai.");
  }

  async getTeacherActivePlannedClassSections(
    req,
    subjectId,
    academicYearId,
    semesterId,
  ) {
    throw new Error("getTeacherClassSections() chưa được triển khai.");
  }
}

module.exports = ClassSectionRepository;
