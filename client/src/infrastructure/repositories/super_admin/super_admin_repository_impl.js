const SuperAdminRepository = require("../../../domain/repositories/super_admin/super_admin_repository");
const SuperAdminApi = require("../../api/super_admin/super_admin_api");

class SuperAdminRepositoryImpl extends SuperAdminRepository {
  async register(data) {
    try {
      const response = await SuperAdminApi.register({
        full_name: data.full_name,
        username: data.username,
        password: data.password,
      });

      if (!response) {
        throw new Error("Server không trả về dữ liệu");
      }

      if (!response.success) {
        throw new Error(response.message || "Đăng ký Super Admin thất bại");
      }

      return response.data;
    } catch (error) {
      console.error("REGISTER SUPER ADMIN ERROR");
      console.error("STATUS:", error.response?.status);
      console.error("DATA:", error.response?.data);
      if (error.response) {
        const data = error.response.data;
        const message =
          data?.message ||
          Object.entries(data || {})
            .map(([field, messages]) => {
              return `${field}: ${
                Array.isArray(messages) ? messages.join(", ") : messages
              }`;
            })
            .join(" | ") ||
          "Đăng ký Super Admin thất bại";
        throw new Error(message);
      }
      throw error;
    }
  }
}

module.exports = SuperAdminRepositoryImpl;
