const AuthRepository = require("../../../domain/repositories/auth/auth_repository");

const authenticateApi = require("../../api/auth/auth_api");

class AuthRepositoryImpl extends AuthRepository {
  async login(data) {
    try {
      const response = await authenticateApi.login(data);

      if (!response) {
        throw new Error("Server không trả về dữ liệu đăng nhập");
      }

      if (!response.success) {
        throw new Error(response.message || "Đăng nhập thất bại");
      }

      if (!response.data) {
        throw new Error("Dữ liệu đăng nhập không hợp lệ");
      }

      if (!response.data.user) {
        throw new Error("Không nhận được thông tin người dùng");
      }

      if (!response.data.access_token) {
        throw new Error("Không nhận được access token");
      }

      if (!response.data.refresh_token) {
        throw new Error("Không nhận được refresh token");
      }

      return response.data;
    } catch (error) {
      if (error.response) {
        throw new Error(error.response.data?.message || "Đăng nhập thất bại");
      }

      throw error;
    }
  }

  async logout(data) {
    try {
      const response = await authenticateApi.logout(data);
      if (!response) {
        throw new Error("Server không trả về dữ liệu đăng xuất");
      }
      if (!response.success) {
        throw new Error(response.message || "Đăng xuất thất bại");
      }
      return response;
    } catch (error) {
      if (error.response) {
        throw new Error(error.response.data?.message || "Đăng xuất thất bại");
      }
      throw error;
    }
  }

  async refreshToken(data) {
    try {
      const response = await authenticateApi.refreshToken(data);
      if (!response) {
        throw new Error("Server không trả về dữ liệu refresh token");
      }
      if (!response.success) {
        throw new Error(response.message || "Refresh token thất bại");
      }
      if (!response.data) {
        throw new Error("Dữ liệu refresh token không hợp lệ");
      }
      if (!response.data.access_token) {
        throw new Error("Không nhận được access token mới");
      }
      if (!response.data.refresh_token) {
        throw new Error("Không nhận được refresh token mới");
      }
      return response.data;
    } catch (error) {
      if (error.response) {
        throw new Error(
          error.response.data?.message || "Refresh token thất bại",
        );
      }

      throw error;
    }
  }
}

module.exports = AuthRepositoryImpl;
