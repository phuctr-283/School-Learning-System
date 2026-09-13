const AcademicYearRepository = require("../../../domain/repositories/academic_year/academic_year_repository");

const AcademicYearDTO = require("../../../application/academic_years/dto/academic_year.dto");

const academicYearApi = require("../../api/academic_year/academic_year_api");

class AcademicYearRepositoryImpl extends AcademicYearRepository {
  async getAcademicYears(req) {
    try {
      const response = await academicYearApi.getAcademicYears(req);

      if (!response.success) {
        throw new Error(response.message || "Không thể lấy danh sách năm học");
      }

      const academicYears = response.data || [];

      return academicYears.map(
        (academicYear) => new AcademicYearDTO(academicYear),
      );
    } catch (error) {
      console.error(
        "GET ACADEMIC YEARS ERROR:",
        error.response?.data || error.message,
      );
      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy danh sách năm học",
      );
    }
  }
  async createAcademicYear(req, dto) {
    try {
      const response = await academicYearApi.createAcademicYear(
        req,
        dto.toJSON(),
      );
      if (!response.success) {
        throw new Error(response.message || "Không thể tạo năm học");
      }
      return response.data;
    } catch (error) {
      console.error(
        "CREATE ACADEMIC YEAR ERROR:",
        error.response?.data || error.message,
      );
      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể tạo năm học",
      );
    }
  }
  async getActiveAndPlannedAcademicYears(req) {
    try {
      const response = await academicYearApi.getActiveAndPlannedAcademicYears(req);
      if (!response.success) {
        throw new Error(response.message || "Không thể lấy danh sách năm học");
      }
      const academicYears = response.data || [];
      return academicYears.map(
        (academicYear) => new AcademicYearDTO(academicYear),
      );
    } catch (error) {
      console.error(
        "GET ACTIVE AND PLANNED ACADEMIC YEARS ERROR:",
        error.response?.data || error.message,
      );
      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy danh sách năm học",
      );
    }
  }
}

module.exports = AcademicYearRepositoryImpl;
