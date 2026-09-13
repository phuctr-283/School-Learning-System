const {
  logoutUserUseCase,
} = require(
  "../../../../infrastructure/dependencies/auth/auth_dependency",
);

const TokenManager = require(
  "../../../../infrastructure/security/token_manager",
);


class LogoutController {
  async logout(req, res) {
    try {
      const refreshToken =
        TokenManager.getRefreshToken(
          req.session,
        );

      if (refreshToken) {
        await logoutUserUseCase.execute({
          refreshToken,
        });
      }
    } catch (error) {
      console.error(
        "LOGOUT ERROR:",
        error.message,
      );
    }

    req.session.destroy((error) => {
      if (error) {
        console.error(
          "SESSION DESTROY ERROR:",
          error,
        );

        return res.redirect("/");
      }

      res.clearCookie("connect.sid");

      return res.redirect("/");
    });
  }
}

module.exports = new LogoutController();