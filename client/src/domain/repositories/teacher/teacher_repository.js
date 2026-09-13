class TeacherRepository {
  async getUniversityTeachers(req) {
    throw new Error("getUniversityTeachers() must be implemented");
  }
  async registerTeacher(data) {
    throw new Error("registerTeacher() must be implemented");
  }
}

module.exports = TeacherRepository;
