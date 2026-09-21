const publicApi = require("./public_api");

const TokenManager = require("../security/token_manager");

const AuthenticationRepositoryImpl = require("../repositories/auth/auth_repository_impl");

const authenticationRepository = new AuthenticationRepositoryImpl();

async function requestWithAuth(req, config) {
  let accessToken = TokenManager.getAccessToken(req.session);

  if (!accessToken) {
    throw new Error("UNAUTHORIZED");
  }

  if (TokenManager.isAccessTokenExpired(accessToken)) {
    const refreshToken = TokenManager.getRefreshToken(req.session);

    if (!refreshToken) {
      TokenManager.clearTokens(req.session);

      delete req.session.user;

      throw new Error("SESSION_EXPIRED");
    }

    try {
      const result = await authenticationRepository.refreshToken({
        refresh_token: refreshToken,
      });

      TokenManager.setTokens(req.session, {
        access_token: result.access_token,

        refresh_token: result.refresh_token || refreshToken,
      });

      accessToken = result.access_token;
    } catch (error) {
      TokenManager.clearTokens(req.session);

      delete req.session.user;

      throw new Error("SESSION_EXPIRED");
    }
  }

  return publicApi.request({
    ...config,

    headers: {
      ...config.headers,

      Authorization: `Bearer ${accessToken}`,
    },
  });
}

const authenticatedApi = {
  request: requestWithAuth,

  async get(req, url, config = {}) {
    return requestWithAuth(req, {
      method: "GET",
      url,
      ...config,
    });
  },

  async post(req, url, data = {}, config = {}) {
    return requestWithAuth(req, {
      method: "POST",
      url,
      data,
      ...config,
    });
  },

  async put(req, url, data = {}, config = {}) {
    return requestWithAuth(req, {
      method: "PUT",
      url,
      data,
      ...config,
    });
  },
  async patch(req, url, data = {}, config = {}) {
    return requestWithAuth(req, {
      method: "PATCH",
      url,
      data,
      ...config,
    });
  },
  async delete(req, url, config = {}) {
    return requestWithAuth(req, {
      method: "DELETE",
      url,
      ...config,
    });
  },
};

module.exports = authenticatedApi;
