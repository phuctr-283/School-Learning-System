class SemesterRepository {
  async getUniversitySemesters(req) {
    throw new Error(
      "getUniversitySemesters() must be implemented",
    );
  }
  async getActivePlanned(req) {

    throw new Error(
      "Method getActivePlanned() must be implemented."
    );
  }
  async createSemester(req, data) {

    throw new Error(
      "createSemester() must be implemented",
    );
  }
}

module.exports = SemesterRepository;