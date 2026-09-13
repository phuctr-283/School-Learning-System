class AcademicYearRepository {
  async getAcademicYears(req) {
    throw new Error("getAcademicYears() must be implemented");
  }
  async createAcademicYear(req, dto) {
    throw new Error("createAcademicYear() must be implemented");
  }
  async getActiveAndPlannedAcademicYears(req) {
    throw new Error(
      "getActiveAndPlannedAcademicYears() must be implemented",
    );
  }
}

module.exports = AcademicYearRepository;
