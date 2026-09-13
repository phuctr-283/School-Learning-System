const SemesterRepository = require("../../../domain/repositories/semester/semester_repository");

const SemesterDTO = require("../../../application/semesters/dto/semester.dto");
const SemesterContentDTO = require("../../../application/semesters/dto/semester_content.dto");
const semesterApi = require("../../api/semester/semester_api");

class SemesterRepositoryImpl extends SemesterRepository {
  async getUniversitySemesters(req) {
    try {
      const response = await semesterApi.getUniversitySemesters(req);

      if (!response.success) {
        throw new Error(response.message || "Không thể lấy danh sách học kỳ");
      }

      const semesters = response.data || [];

      return semesters.map((semester) => new SemesterDTO(semester));
    } catch (error) {
      console.error(
        "GET UNIVERSITY SEMESTERS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy danh sách học kỳ",
      );
    }
  }
  // =========================================
  // GET ACTIVE / PLANNED SEMESTERS
  // =========================================

  async getActivePlanned(req) {
    try {
      const response = await semesterApi.getActivePlanned(req);

      if (!response.success) {
        throw new Error(
          response.message ||
            "Không thể lấy danh sách học kỳ đang hoạt động hoặc đã lên kế hoạch.",
        );
      }

      const semesters = response.data || [];

      return semesters.map((semester) => new SemesterContentDTO(semester));
    } catch (error) {
      console.error(
        "GET ACTIVE PLANNED SEMESTERS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy danh sách học kỳ.",
      );
    }
  }
  async createSemester(req, data) {
    try {
      const response = await semesterApi.createSemester(req, data.toJSON());

      if (!response.success) {
        throw new Error(response.message || "Không thể tạo học kỳ");
      }

      return new SemesterDTO(response.data);
    } catch (error) {
      console.error(
        "CREATE SEMESTER ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể tạo học kỳ",
      );
    }
  }
}

module.exports = SemesterRepositoryImpl;
