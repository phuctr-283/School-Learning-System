class AuthRepository {
  async login(dto) {
    throw new Error(
      "AuthRepository.login() chưa được implement"
    );
  }

  async logout(dto) {
    throw new Error(
      "AuthRepository.logout() chưa được implement"
    );
  }

  async refreshToken(dto) {
    throw new Error(
      "AuthRepository.refreshToken() chưa được implement"
    );
  }
}

module.exports = AuthRepository;