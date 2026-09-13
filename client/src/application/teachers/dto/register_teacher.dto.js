class RegisterTeacherDTO {
  constructor({
    full_name,
    university_id,
    department_id,
    email,
    password,
    confirmPassword,
  }) {
    this.fullName = full_name?.trim();

    this.universityId = university_id?.trim();

    this.departmentId = department_id?.trim();

    this.email = email?.trim().toLowerCase();

    this.password = password;

    this.confirmPassword = confirmPassword;
  }

  toJSON() {
    return {
      full_name: this.fullName,

      university_id: this.universityId,

      department_id: this.departmentId,

      email: this.email,

      password: this.password,

      confirm_password: this.confirmPassword,
    };
  }
}

module.exports = RegisterTeacherDTO;
