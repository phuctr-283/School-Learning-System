const TokenManager = require("../../../infrastructure/security/token_manager");
const RefreshTokenUseCase = require("../../../application/auth/use_cases/refresh_token");
const AuthRepositoryImpl = require("../../../infrastructure/repositories/auth/auth_repository_impl");
const authRepository = new AuthRepositoryImpl();

const refreshTokenUseCase = new RefreshTokenUseCase(authRepository);

async function authMiddleware(req, res, next) {
  try {
    const accessToken = TokenManager.getAccessToken(req.session);
    const refreshToken = TokenManager.getRefreshToken(req.session);

    if (!accessToken && !refreshToken) {
      return res.redirect("/");
    }

    if (accessToken && !TokenManager.isAccessTokenExpired(accessToken)) {
      return next();
    }
    if (!refreshToken) {
      clearAuthentication(req);
      return res.redirect("/");
    }
    const result = await refreshTokenUseCase.execute({
      refreshToken,
    });
    TokenManager.setTokens(req.session, {
      access_token: result.access_token,
      refresh_token: result.refresh_token || refreshToken,
    });
    return next();
  } catch (error) {
    console.error("AUTH MIDDLEWARE ERROR:", error.message);
    clearAuthentication(req);
    return res.redirect("/");
  }
}

function clearAuthentication(req) {
  TokenManager.clearTokens(req.session);
  delete req.session.user;
}

module.exports = authMiddleware;
