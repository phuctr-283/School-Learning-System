const RegisterSchoolAdminDTO = require("../dto/register_school_admin.dto");
const UsernamePolicy = require("../../../domain/services/username_policy");

class RegisterSchoolAdminUseCase {
  constructor(schoolAdminRepository) {
    this.schoolAdminRepository = schoolAdminRepository;
  }

  async execute(data) {
    const dto = new RegisterSchoolAdminDTO(data);
    if (!dto.fullName?.trim()) {
      throw new Error("Họ và tên không được để trống");
    }
    const username = UsernamePolicy.normalize(dto.username);
    if (!username) {
      throw new Error("Tên đăng nhập không được để trống");
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
    const universityDomain = UsernamePolicy.extractSchoolDomain(username);
    if (!universityDomain) {
      throw new Error("Username School Admin phải có dạng @admin.{domain}");
    }
    if (UsernamePolicy.validateSuperAdmin(username)) {
      throw new Error("Username này thuộc Super Admin");
    }

    return this.schoolAdminRepository.register({
      full_name: dto.fullName.trim(),
      username,
      password: dto.password,
    });
  }
}

module.exports = RegisterSchoolAdminUseCase;
