const AssignmentRepository = require("../../../domain/repositories/assignment/assignment_repository");

const assignmentApi = require("../../api/assignment/assignment_api");

const AssignmentListDTO = require("../../../application/assignments/dto/assignment_list.dto");

const AssignmentContentDTO = require("../../../application/assignments/dto/assignment_content.dto");
class AssignmentRepositoryImpl extends AssignmentRepository {
  async createAssignment(req, assignmentDTO) {
    try {
      if (!assignmentDTO || typeof assignmentDTO.toRequest !== "function") {
        throw new Error("Dữ liệu tạo bài tập không hợp lệ.");
      }
      const payload = assignmentDTO.toRequest();
      const response = await assignmentApi.createAssignment(req, payload);
      if (!response || response.success !== true) {
        throw new Error(response?.message || "Không thể tạo bài tập.");
      }
      return response.data;
    } catch (error) {
      const backendData = error.response?.data;
      console.error("CREATE ASSIGNMENT ERROR:", backendData || error.message);
      if (backendData?.message) {
        throw new Error(backendData.message);
      }
      if (backendData?.errors) {
        throw new Error(this.formatValidationErrors(backendData.errors));
      }
      throw new Error(error.message || "Không thể tạo bài tập.");
    }
  }
  async updateAssignment(req, assignmentDTO) {
    try {
      if (!assignmentDTO || typeof assignmentDTO.toRequest !== "function") {
        throw new Error("Dữ liệu cập nhật bài tập không hợp lệ.");
      }
      const payload = assignmentDTO.toRequest();
      console.log("========== UPDATE ASSIGNMENT ==========");
      console.log("ASSIGNMENT ID:", assignmentDTO.assignmentId);
      console.log("UPDATE PAYLOAD:", JSON.stringify(payload, null, 2));
      const response = await assignmentApi.updateAssignment(
        req,
        assignmentDTO.assignmentId,
        payload,
      );
      console.log("========== NODE UPDATE RESPONSE ==========");
      console.log(JSON.stringify(response, null, 2));
      if (!response || response.success !== true) {
        throw new Error(response?.message || "Không thể cập nhật bài tập.");
      }
      return response.data;
    } catch (error) {
      console.error("========== NODE UPDATE ERROR ==========");

      console.error("STATUS:", error.response?.status);

      console.error("DATA:", JSON.stringify(error.response?.data, null, 2));

      console.error("MESSAGE:", error.message);

      console.error("========================================");

      const backendData = error.response?.data;

      if (backendData?.message) {
        throw new Error(backendData.message);
      }

      if (backendData?.errors) {
        throw new Error(this.formatValidationErrors(backendData.errors));
      }

      throw new Error(error.message || "Không thể cập nhật bài tập.");
    }
  }
  formatValidationErrors(errors) {
    if (!errors || typeof errors !== "object") {
      return "Dữ liệu không hợp lệ.";
    }

    return Object.entries(errors)
      .map(([field, messages]) => {
        const value = Array.isArray(messages)
          ? messages.join(", ")
          : String(messages);

        return `${field}: ${value}`;
      })
      .join(" | ");
  }

  async getAssignments(req) {
    try {
      const response = await assignmentApi.getAssignments(req);

      if (!response || response.success !== true) {
        throw new Error(
          response?.message || "Không thể tải danh sách bài tập.",
        );
      }

      return (response.data || []).map((item) =>
        AssignmentListDTO.fromResponse(item),
      );
    } catch (error) {
      console.error(
        "GET ASSIGNMENTS ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể tải danh sách bài tập.",
      );
    }
  }
  async getAssignmentsBySubject(req, subjectId) {
    try {
      if (!subjectId) {
        throw new Error("Không xác định được môn học.");
      }

      const response = await assignmentApi.getAssignmentsBySubject(
        req,
        subjectId,
      );

      if (!response || response.success !== true) {
        throw new Error(
          response?.message || "Không thể tải bài tập của môn học.",
        );
      }

      return (response.data || []).map((item) =>
        AssignmentListDTO.fromResponse(item),
      );
    } catch (error) {
      console.error(
        "GET ASSIGNMENTS BY SUBJECT ERROR:",
        error.response?.data || error.message,
      );

      throw new Error(
        error.response?.data?.message ||
          error.message ||
          "Không thể tải bài tập của môn học.",
      );
    }
  }
  async getAssignmentById(req, assignmentId) {
    try {
      const id = String(assignmentId ?? "").trim();

      if (!id) {
        throw new Error("Thiếu mã bài tập.");
      }

      const response = await assignmentApi.getAssignmentById(req, id);

      if (!response || response.success !== true) {
        throw new Error(response?.message || "Không thể tải bài tập.");
      }

      if (!response.data) {
        throw new Error("Dữ liệu bài tập không tồn tại.");
      }

      return response.data;
    } catch (error) {
      const backendData = error.response?.data;

      console.error("GET ASSIGNMENT ERROR:", backendData || error.message);

      if (backendData?.message) {
        throw new Error(backendData.message);
      }

      if (backendData?.errors) {
        throw new Error(this.formatValidationErrors(backendData.errors));
      }

      throw new Error(error.message || "Không thể tải bài tập.");
    }
  }
}

module.exports = AssignmentRepositoryImpl;
