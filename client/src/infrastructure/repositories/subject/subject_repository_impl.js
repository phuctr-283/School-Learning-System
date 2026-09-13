const SubjectRepository = require("../../../domain/repositories/subject/subject_repository");

const SubjectDTO = require("../../../application/subjects/dto/subject.dto");

const subjectApi = require("../../api/subject/subject_api");

class SubjectRepositoryImpl extends SubjectRepository {
  async getUniversitySubjects(req) {
    try {
      const response = await subjectApi.getUniversitySubjects(req);

      if (!response.success) {
        throw new Error(response.message || "Không thể lấy danh sách môn học.");
      }

      const subjects = response.data || [];

      return subjects.map((subject) => new SubjectDTO(subject));
    } catch (error) {
      console.error(
        "GET UNIVERSITY SUBJECTS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy danh sách môn học.",
      );
    }
  }
  async createSubject(req, data) {
    try {
      const response = await subjectApi.createSubject(req, data.toJSON());

      if (!response.success) {
        throw new Error(response.message || "Không thể tạo môn học.");
      }

      return new SubjectDTO(response.data);
    } catch (error) {
      console.error(
        "CREATE SUBJECT ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể tạo môn học.",
      );
    }
  }
}

module.exports = SubjectRepositoryImpl;
