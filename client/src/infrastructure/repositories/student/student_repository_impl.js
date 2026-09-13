const StudentRepository = require("../../../domain/repositories/student/student_repository");

const StudentDTO = require("../../../application/students/dto/student.dto");

const studentApi = require("../../api/student/student_api");

class StudentRepositoryImpl extends StudentRepository {
  async getUniversityStudents(req) {
    try {
      const response = await studentApi.getUniversityStudents(req);

      if (!response.success) {
        throw new Error(
          response.message || "Không thể lấy danh sách sinh viên.",
        );
      }

      return (response.data || []).map((student) => new StudentDTO(student));
    } catch (error) {
      console.error(
        "GET UNIVERSITY STUDENTS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy danh sách sinh viên.",
      );
    }
  }
  async importStudents(req, file) {
    try {
      const response = await studentApi.importStudents(req, file);

      if (!response.success) {
        throw new Error(response.message || "Không thể import sinh viên.");
      }

      return response.data;
    } catch (error) {
      console.error(
        "IMPORT STUDENTS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể import sinh viên.",
      );
    }
  }
}

module.exports = StudentRepositoryImpl;
