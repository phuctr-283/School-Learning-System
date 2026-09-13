class StudentRepository {
  async getUniversityStudents(req) {
    throw new Error("getUniversityStudents() must be implemented");
  }
  async importStudents(req, file) {
    throw new Error("importStudents() must be implemented");
  }
}

module.exports = StudentRepository;
