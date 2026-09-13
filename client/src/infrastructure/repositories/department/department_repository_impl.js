const DepartmentRepository = require("../../../domain/repositories/department/department_repository");

const DepartmentDTO = require("../../../application/departments/dto/department.dto");
const ActiveDepartmentDTO = require("../../../application/departments/dto/active_department.dto");
const departmentApi = require("../../api/department/department_api");

class DepartmentRepositoryImpl extends DepartmentRepository {
  async getUniversityDepartments(req) {
    try {
      const response = await departmentApi.getUniversityDepartments(req);
      if (!response.success) {
        throw new Error(response.message || "Không thể lấy danh sách khoa");
      }
      const departments = response.data || [];
      return departments.map((department) => new DepartmentDTO(department));
    } catch (error) {
      console.error(
        "GET UNIVERSITY DEPARTMENTS ERROR:",
        error.response?.data || error.message,
      );
      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy danh sách khoa",
      );
    }
  }

  async create(req, dto) {
    try {
      const response = await departmentApi.create(req, {
        department_id: dto.departmentId,
        department_number: dto.departmentNumber,
        name: dto.name,
        head_id: dto.headId,
      });

      if (!response.success) {
        throw new Error(response.message || "Tạo khoa thất bại");
      }
      return new DepartmentDTO(response.data);
    } catch (error) {
      console.error(
        "CREATE DEPARTMENT ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message || error.message || "Tạo khoa thất bại",
      );
    }
  }
  async getActiveDepartments(universityId) {
    try {
      const response = await departmentApi.getActiveDepartments(universityId);

      if (!response.success) {
        throw new Error(response.message || "Không thể lấy danh sách khoa");
      }

      const departments = response.data || [];

      return departments.map(
        (department) => new ActiveDepartmentDTO(department),
      );
    } catch (error) {
      console.error(
        "GET ACTIVE DEPARTMENTS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy danh sách khoa",
      );
    }
  }
  async getActivesDepartments(req) {
    try {
      const response = await departmentApi.getActivesDepartments(req);

      if (!response.success) {
        throw new Error(response.message || "Không thể lấy danh sách khoa.");
      }

      const departments = response.data || [];

      return departments.map((department) => new DepartmentDTO(department));
    } catch (error) {
      console.error(
        "GET ACTIVE DEPARTMENTS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy danh sách khoa.",
      );
    }
  }
}

module.exports = DepartmentRepositoryImpl;
