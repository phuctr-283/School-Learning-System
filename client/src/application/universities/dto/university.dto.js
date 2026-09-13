class UniversityDTO {
  constructor({
    university_id,
    name,
    domain,
    email,
    phone,
    is_active,
    updated_at,
  }) {
    this.universityId = university_id;
    this.name = name;
    this.domain = domain;
    this.email = email;
    this.phone = phone;
    this.isActive = is_active;
    this.updatedAt = updated_at;
  }
}

module.exports = UniversityDTO;