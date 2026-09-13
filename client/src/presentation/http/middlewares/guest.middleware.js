const TokenManager = require("../../../infrastructure/security/token_manager");
const AccountLevel = require("../../../domain/enums/account_level");
const RefreshTokenUseCase = require("../../../application/auth/use_cases/refresh_token");
const authenticateApi = require("../../../infrastructure/api/auth/auth_api");
const refreshTokenUseCase = new RefreshTokenUseCase(authenticateApi);

async function guestMiddleware(req, res, next) {
  try {
    const user = req.session?.user || null;

    const accessToken = TokenManager.getAccessToken(req.session);

    const refreshToken = TokenManager.getRefreshToken(req.session);

    if (!accessToken && !refreshToken) {
      delete req.session.user;

      return next();
    }

    if (accessToken && !TokenManager.isAccessTokenExpired(accessToken)) {
      return redirectByAccountLevel(res, user);
    }

    if (refreshToken) {
      try {
        const result = await refreshTokenUseCase.execute({
          refreshToken,
        });

        TokenManager.setTokens(req.session, {
          access_token: result.access_token,
          refresh_token: result.refresh_token || refreshToken,
        });

        return redirectByAccountLevel(res, req.session.user);
      } catch (error) {
        console.error("GUEST REFRESH TOKEN ERROR:", error.message);

        clearAuthentication(req);

        return next();
      }
    }

    clearAuthentication(req);

    return next();
  } catch (error) {
    console.error("GUEST MIDDLEWARE ERROR:", error.message);

    clearAuthentication(req);

    return next();
  }
}

function redirectByAccountLevel(res, user) {
  if (!user) {
    return res.redirect("/");
  }

  switch (user.account_level) {
    case AccountLevel.SUPER_ADMIN:
      return res.redirect("/super-admin");

    case AccountLevel.SCHOOL_ADMIN:
      return res.redirect("/school-admin");

    case AccountLevel.TEACHER:
      return res.redirect("/teacher");

    case AccountLevel.STUDENT:
      return res.redirect("/student");

    default:
      return res.redirect("/");
  }
}

function clearAuthentication(req) {
  TokenManager.clearTokens(req.session);

  delete req.session.user;
}

module.exports = guestMiddleware;
