const UniversityRepository = require("../../../domain/repositories/university/university_repository");

const UniversityDTO = require("../../../application/universities/dto/university.dto");
const ActiveUniversityDTO = require("../../../application/universities/dto/active_university.dto");
const universityApi = require("../../api/university/university_api");

class UniversityRepositoryImpl extends UniversityRepository {
  async create(req, data) {
    try {
      const response = await universityApi.create(req, data);

      if (!response) {
        throw new Error("Server không trả về dữ liệu");
      }

      if (!response.success) {
        throw new Error(response.message || "Tạo trường thất bại");
      }

      if (!response.data) {
        throw new Error("Dữ liệu trường không hợp lệ");
      }

      return new UniversityDTO(response.data);
    } catch (error) {
      if (error.response) {
        throw new Error(error.response.data?.message || "Tạo trường thất bại");
      }

      throw error;
    }
  }

  async getAll(req) {
    try {
      const response = await universityApi.getAll(req);

      if (!response) {
        throw new Error("Server không trả về dữ liệu");
      }

      if (!response.success) {
        throw new Error(response.message || "Không thể lấy danh sách trường");
      }

      return (response.data || []).map(
        (university) => new UniversityDTO(university),
      );
    } catch (error) {
      if (error.response) {
        throw new Error(
          error.response.data?.message || "Không thể lấy danh sách trường",
        );
      }

      throw error;
    }
  }
  async getActiveUniversities() {
    try {
      const response = await universityApi.getActiveUniversities();

      if (!response.success) {
        throw new Error(response.message || "Không thể lấy danh sách trường");
      }

      return (response.data || []).map(
        (university) => new ActiveUniversityDTO(university),
      );
    } catch (error) {
      console.error(
        "GET ACTIVE UNIVERSITIES ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy danh sách trường",
      );
    }
  }
}

module.exports = UniversityRepositoryImpl;
