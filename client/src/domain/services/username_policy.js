class UsernamePolicy {
  static SUPER_ADMIN_DOMAIN = "admin.vn";

  static SCHOOL_ADMIN_PREFIX = "admin.";

  // =========================================
  // NORMALIZE
  // =========================================

  static normalize(username) {
    return String(username || "")
      .trim()
      .toLowerCase();
  }

  // =========================================
  // SUPER ADMIN
  // =========================================

  static validateSuperAdmin(username) {
    username = this.normalize(username);

    return username.endsWith(`@${this.SUPER_ADMIN_DOMAIN}`);
  }

  // =========================================
  // EXTRACT SCHOOL DOMAIN
  // =========================================

  static extractSchoolDomain(username) {
    username = this.normalize(username);

    if (!username.includes("@")) {
      return null;
    }

    const domain = username.split("@", 2)[1];

    if (!domain.startsWith(this.SCHOOL_ADMIN_PREFIX)) {
      return null;
    }

    const universityDomain = domain.substring(this.SCHOOL_ADMIN_PREFIX.length);

    return universityDomain || null;
  }

  // =========================================
  // SCHOOL ADMIN
  // =========================================

  static validateSchoolAdmin(username, universityDomain) {
    username = this.normalize(username);

    universityDomain = String(universityDomain || "")
      .trim()
      .toLowerCase();

    return username.endsWith(`@admin.${universityDomain}`);
  }

  // =========================================
  // GET ACCOUNT TYPE
  // =========================================

  static getAccountType(username) {
    username = this.normalize(username);

    if (this.validateSuperAdmin(username)) {
      return "super_admin";
    }

    if (this.extractSchoolDomain(username)) {
      return "school_admin";
    }

    return null;
  }
}

module.exports = UsernamePolicy;
