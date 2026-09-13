class CreateUniversityDTO {
  constructor({
    university_id,
    name,
    domain,
    email,
    phone,
  }) {
    this.universityId = university_id;
    this.name = name;
    this.domain = domain;
    this.email = email;
    this.phone = phone;
  }
}

module.exports = CreateUniversityDTO;