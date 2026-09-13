const CreateUniversityDTO = require(
  "../dto/create_university.dto"
);

class CreateUniversityUseCase {
  constructor(universityRepository) {
    this.universityRepository = universityRepository;
  }

  async execute(data, req) {
    const dto = new CreateUniversityDTO(data);

    // =========================================
    // UNIVERSITY ID
    // =========================================

    if (!dto.universityId?.trim()) {
      throw new Error(
        "Mã trường không được để trống"
      );
    }

    if (dto.universityId.length > 50) {
      throw new Error(
        "Mã trường không được vượt quá 50 ký tự"
      );
    }

    // =========================================
    // NAME
    // =========================================

    if (!dto.name?.trim()) {
      throw new Error(
        "Tên trường không được để trống"
      );
    }

    // =========================================
    // DOMAIN
    // =========================================

    if (!dto.domain?.trim()) {
      throw new Error(
        "Domain không được để trống"
      );
    }

    // =========================================
    // EMAIL
    // =========================================

    if (!dto.email?.trim()) {
      throw new Error(
        "Email không được để trống"
      );
    }

    // =========================================
    // PHONE
    // =========================================

    if (!dto.phone?.trim()) {
      throw new Error(
        "Số điện thoại không được để trống"
      );
    }

    // =========================================
    // CREATE
    // =========================================

    return this.universityRepository.create(
      req,
      {
        university_id: dto.universityId.trim(),
        name: dto.name.trim(),
        domain: dto.domain.trim().toLowerCase(),
        email: dto.email.trim().toLowerCase(),
        phone: dto.phone.trim(),
      }
    );
  }
}

module.exports = CreateUniversityUseCase;