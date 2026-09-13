class TokenManager {
  static setTokens(session, tokens) {
    if (!session) {
      throw new Error("Session không tồn tại");
    }
    if (!tokens?.access_token) {
      throw new Error("Access token không tồn tại");
    }
    session.tokens = {
      accessToken: tokens.access_token,
      refreshToken: tokens.refresh_token || null,
    };
  }
  static getAccessToken(session) {
    return session?.tokens?.accessToken || null;
  }
  static getRefreshToken(session) {
    return session?.tokens?.refreshToken || null;
  }
  static clearTokens(session) {
    if (session) {
      delete session.tokens;
    }
  }
  static decodePayload(token) {
    if (!token) {
      return null;
    }
    try {
      const parts = token.split(".");
      if (parts.length !== 3) {
        return null;
      }
      return JSON.parse(Buffer.from(parts[1], "base64url").toString());
    } catch (error) {
      return null;
    }
  }

  static isAccessTokenExpired(token) {
    const payload = this.decodePayload(token);
    if (!payload?.exp) {
      return true;
    }
    const currentTime = Math.floor(Date.now() / 1000);
    return payload.exp <= currentTime;
  }
}

module.exports = TokenManager;
