const LogoutDTO = require("../dto/logout.dto");

class LogoutUserUseCase {
  constructor(authRepository) {
    this.authRepository = authRepository;
  }

  async execute(data) {
    const dto = new LogoutDTO(data);
    if (!dto.refreshToken) {
      throw new Error("Refresh token không được để trống");
    }
    try {
      return await this.authRepository.logout({
        refresh_token: dto.refreshToken,
      });
    } catch (error) {
      throw new Error(error.message || "Đăng xuất thất bại");
    }
  }
}

module.exports = LogoutUserUseCase;
