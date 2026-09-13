const TeacherRepository = require("../../../domain/repositories/teacher/teacher_repository");

const TeacherDTO = require("../../../application/teachers/dto/teacher.dto");
const RegisterTeacherDTO = require("../../../application/teachers/dto/register_teacher.dto");
const teacherApi = require("../../api/teacher/teacher_api");

class TeacherRepositoryImpl extends TeacherRepository {
  async getUniversityTeachers(req) {
    try {
      const response = await teacherApi.getUniversityTeachers(req);

      if (!response.success) {
        throw new Error(
          response.message || "Không thể lấy danh sách giảng viên",
        );
      }

      const teachers = response.data || [];

      return teachers.map((teacher) => new TeacherDTO(teacher));
    } catch (error) {
      console.error(
        "GET UNIVERSITY TEACHERS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy danh sách giảng viên",
      );
    }
  }
  async registerTeacher(data) {
    try {
      const response = await teacherApi.registerTeacher(data.toJSON());

      if (!response.success) {
        throw new Error(response.message || "Đăng ký giảng viên thất bại");
      }

      return response.data;
    } catch (error) {
      console.error(
        "REGISTER TEACHER ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Đăng ký giảng viên thất bại",
      );
    }
  }
}

module.exports = TeacherRepositoryImpl;
