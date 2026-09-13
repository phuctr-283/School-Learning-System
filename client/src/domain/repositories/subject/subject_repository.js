class SubjectRepository {
  async getUniversitySubjects(req) {
    throw new Error(
      "getUniversitySubjects() must be implemented",
    );
  }
  async createSubject(req, data) {
    throw new Error(
      "createSubject() must be implemented",
    );
  }
}

module.exports = SubjectRepository;