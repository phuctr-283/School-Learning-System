class SchoolAdminDTO {
  constructor({
    admin_id,
    full_name,
    gender,
    email,
    phone,
    university_id,
    university_name,
    status,
  }) {
    this.adminId = admin_id;
    this.fullName = full_name;
    this.gender = gender;
    this.email = email;
    this.phone = phone;

    this.universityId = university_id;
    this.universityName = university_name;

    this.status = status;
  }
}

module.exports = SchoolAdminDTO;
