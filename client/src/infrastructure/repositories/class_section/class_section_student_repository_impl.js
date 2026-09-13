const ClassSectionStudentRepository = require("../../../domain/repositories/class_section/class_section_student_repository");

const classSectionStudentApi = require("../../api/class_section/class_section_api");

const StudentImportResultDTO = require("../../../application/class_sections/dto/student_import_result.dto");

class ClassSectionStudentRepositoryImpl extends ClassSectionStudentRepository {
  async importStudents(req, file) {
    const response = await classSectionStudentApi.importStudents(req, file);

    if (!response || response.success !== true) {
      throw new Error(response?.message || "Import sinh viên thất bại");
    }

    return StudentImportResultDTO.fromResponse(response.data);
  }

  async getStudents(req, params) {
    const response = await classSectionStudentApi.getStudents(req, params);

    if (!response || response.success !== true) {
      throw new Error(response?.message || "Không thể tải danh sách sinh viên");
    }

    return response.data;
  }
}

module.exports = ClassSectionStudentRepositoryImpl;
