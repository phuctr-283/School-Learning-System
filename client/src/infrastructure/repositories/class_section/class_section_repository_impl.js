const ClassSectionRepository = require("../../../domain/repositories/class_section/class_section_repository");

const ClassSectionDTO = require("../../../application/class_sections/dto/class_section.dto");

const TeacherSubjectDTO = require("../../../application/class_sections/dto/teacher_subject.dto");

const TeacherClassSectionDTO = require("../../../application/class_sections/dto/teacher_class_section.dto");

const classSectionApi = require("../../api/class_section/class_section_api");

class ClassSectionRepositoryImpl extends ClassSectionRepository {
  async getUniversityClassSections(req) {
    try {
      const response = await classSectionApi.getUniversityClassSections(req);

      if (!response.success) {
        throw new Error(
          response.message || "Không thể lấy danh sách lớp học phần.",
        );
      }

      return (response.data || []).map(
        (classSection) => new ClassSectionDTO(classSection),
      );
    } catch (error) {
      console.error(
        "GET UNIVERSITY CLASS SECTIONS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể lấy danh sách lớp học phần.",
      );
    }
  }
  async importClassSections(req, file) {
    try {
      const response = await classSectionApi.importClassSections(req, file);

      if (!response.success) {
        throw new Error(response.message || "Không thể import lớp học phần.");
      }

      return {
        createdCount: response.data?.created_count || 0,

        skippedCount: response.data?.skipped_count || 0,

        skippedItems: response.data?.skipped_items || [],

        message: response.message || "Import lớp học phần thành công.",
      };
    } catch (error) {
      console.error(
        "IMPORT CLASS SECTIONS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể import lớp học phần.",
      );
    }
  }
  async getTeacherSubjects(req) {
    const response = await classSectionApi.getTeacherSubjects(req);

    if (!response || response.success !== true) {
      throw new Error(response?.message || "Không thể tải danh sách môn học.");
    }

    return (response.data || []).map((item) =>
      TeacherSubjectDTO.fromResponse(item),
    );
  }

  async getTeacherClassSections(req, subjectId) {
    const response = await classSectionApi.getTeacherClassSections(
      req,
      subjectId,
    );

    if (!response || response.success !== true) {
      throw new Error(
        response?.message || "Không thể tải danh sách lớp học phần.",
      );
    }

    return (response.data || []).map((item) =>
      TeacherClassSectionDTO.fromResponse(item),
    );
  }
}

module.exports = ClassSectionRepositoryImpl;
