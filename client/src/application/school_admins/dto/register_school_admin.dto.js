class RegisterSchoolAdminDTO {
  constructor({ full_name, username, password }) {
    this.fullName = full_name;
    this.username = username;
    this.password = password;
  }
}

module.exports = RegisterSchoolAdminDTO;
