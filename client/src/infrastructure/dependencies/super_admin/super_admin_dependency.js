const SuperAdminRepositoryImpl = require(
  "../../repositories/super_admin/super_admin_repository_impl",
);

const RegisterSuperAdminUseCase = require(
  "../../../application/super_admins/use_cases/register_super_admin",
);


// Repository
const superAdminRepository =
  new SuperAdminRepositoryImpl();


// Use case
const registerSuperAdminUseCase =
  new RegisterSuperAdminUseCase(
    superAdminRepository,
  );


// Export
module.exports = {
  superAdminRepository,

  registerSuperAdminUseCase,
};