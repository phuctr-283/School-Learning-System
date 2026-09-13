const {
  refreshTokenUseCase,
} = require(
  "../../../../infrastructure/dependencies/auth/auth_dependency",
);

const TokenManager = require(
  "../../../../infrastructure/security/token_manager",
);


class RefreshController {
  async refresh(req, res) {
    try {
      const refreshToken =
        TokenManager.getRefreshToken(
          req.session,
        );

      if (!refreshToken) {
        TokenManager.clearTokens(
          req.session,
        );

        delete req.session.user;

        return res.redirect("/");
      }

      const result =
        await refreshTokenUseCase.execute({
          refreshToken,
        });

      TokenManager.setTokens(
        req.session,
        {
          access_token: result.access_token,
          refresh_token: result.refresh_token,
        },
      );

      return res.redirect(
        req.get("Referrer") || "/",
      );
    } catch (error) {
      console.error(
        "REFRESH ERROR:",
        error.message,
      );

      TokenManager.clearTokens(
        req.session,
      );

      delete req.session.user;

      return res.redirect("/");
    }
  }
}

module.exports = new RefreshController();