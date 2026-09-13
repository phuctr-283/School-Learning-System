const LoginDTO = require("../dto/login.dto");

class LoginUserUseCase {
  constructor(authRepository) {
    this.authRepository = authRepository;
  }

  async execute(data) {
    const dto = new LoginDTO(data);

    if (!dto.username) {
      throw new Error("Tên đăng nhập không được để trống");
    }

    if (dto.username.length > 100) {
      throw new Error("Tên đăng nhập không được vượt quá 100 ký tự");
    }

    if (!dto.password) {
      throw new Error("Mật khẩu không được để trống");
    }

    if (dto.password.length < 8) {
      throw new Error("Mật khẩu phải có ít nhất 8 ký tự");
    }

    if (dto.password.length > 20) {
      throw new Error("Mật khẩu không được vượt quá 20 ký tự");
    }

    let result;

    try {
      result = await this.authRepository.login({
        username: dto.username,
        password: dto.password,
      });
    } catch (error) {
      throw new Error(error.message || "Đăng nhập thất bại");
    }

    if (!result) {
      throw new Error("Không nhận được dữ liệu đăng nhập");
    }

    if (!result.user) {
      throw new Error("Không nhận được thông tin người dùng");
    }

    if (!result.access_token) {
      throw new Error("Access token không tồn tại");
    }

    if (!result.refresh_token) {
      throw new Error("Refresh token không tồn tại");
    }

    return result;
  }
}

module.exports = LoginUserUseCase;
