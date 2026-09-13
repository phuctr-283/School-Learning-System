const RefreshTokenDTO = require("../dto/refresh_token.dto");

class RefreshTokenUseCase {
  constructor(authRepository) {
    this.authRepository = authRepository;
  }

  async execute(data) {
    const dto = new RefreshTokenDTO(data);

    if (!dto.refreshToken) {
      throw new Error("Refresh token không được để trống");
    }

    if (dto.refreshToken.length < 10) {
      throw new Error("Refresh token không hợp lệ");
    }

    let result;

    try {
      result = await this.authRepository.refreshToken({
        refresh_token: dto.refreshToken,
      });
    } catch (error) {
      throw new Error(error.message || "Refresh token thất bại");
    }

    if (!result) {
      throw new Error("Không nhận được dữ liệu refresh token");
    }

    if (!result.access_token) {
      throw new Error("Không nhận được access token mới");
    }

    if (!result.refresh_token) {
      throw new Error("Không nhận được refresh token mới");
    }

    return result;
  }
}

module.exports = RefreshTokenUseCase;
