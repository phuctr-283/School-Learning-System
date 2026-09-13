const SchoolAdminRepository = require("../../../domain/repositories/school_admin/school_admin_repository");
const SchoolAdminApi = require("../../api/school_admin/school_admin_api");
const SchoolAdminDTO = require("../../../application/school_admins/dto/school_admin.dto");

class SchoolAdminRepositoryImpl extends SchoolAdminRepository {
  async getAll(req) {
    try {
      const response = await SchoolAdminApi.getAll(req);

      if (!response) {
        throw new Error("Server không trả về dữ liệu");
      }

      if (!response.success) {
        throw new Error(response.message || "Không thể lấy danh sách Admin");
      }

      return (response.data || []).map(
        (school_admin) => new SchoolAdminDTO(school_admin),
      );
    } catch (error) {
      if (error.response) {
        throw new Error(
          error.response.data?.message || "Không thể lấy danh sách Admin",
        );
      }

      throw error;
    }
  }
  async register(data) {
    try {
      const response = await SchoolAdminApi.register({
        full_name: data.full_name,
        username: data.username,
        password: data.password,
      });

      if (!response) {
        throw new Error("Server không trả về dữ liệu");
      }

      if (!response.success) {
        throw new Error(response.message || "Đăng ký School Admin thất bại");
      }

      return response.data;
    } catch (error) {
      if (error.response) {
        throw new Error(
          error.response.data?.message || "Đăng ký School Admin thất bại",
        );
      }

      throw error;
    }
  }
}

module.exports = SchoolAdminRepositoryImpl;
