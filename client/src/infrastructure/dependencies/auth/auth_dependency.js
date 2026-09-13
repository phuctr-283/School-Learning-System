const LoginUserUseCase = require(
  "../../../application/auth/use_cases/login_user",
);

const LogoutUserUseCase = require(
  "../../../application/auth/use_cases/logout_user",
);

const RefreshTokenUseCase = require(
  "../../../application/auth/use_cases/refresh_token",
);

const AuthRepositoryImpl = require(
  "../../repositories/auth/auth_repository_impl",
);


// Repository
const authRepository =
  new AuthRepositoryImpl();


// Use cases
const loginUserUseCase =
  new LoginUserUseCase(
    authRepository,
  );

const logoutUserUseCase =
  new LogoutUserUseCase(
    authRepository,
  );

const refreshTokenUseCase =
  new RefreshTokenUseCase(
    authRepository,
  );


// Export
module.exports = {
  authRepository,

  loginUserUseCase,
  logoutUserUseCase,
  refreshTokenUseCase,
};