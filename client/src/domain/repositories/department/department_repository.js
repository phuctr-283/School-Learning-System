class DepartmentRepository {
  async getUniversityDepartments(req) {
    throw new Error("getUniversityDepartments() must be implemented");
  }

  async create(req, dto) {
    throw new Error("create() must be implemented");
  }
  async getActiveDepartments(universityId) {
    throw new Error("getActiveDepartments() must be implemented");
  }
  async getActivesDepartments(req) {
    throw new Error(
      "getActiveDepartments() must be implemented",
    );
  }
}

module.exports = DepartmentRepository;
