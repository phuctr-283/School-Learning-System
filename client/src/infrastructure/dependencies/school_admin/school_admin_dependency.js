const SchoolAdminRepositoryImpl = require(
  "../../repositories/school_admin/school_admin_repository_impl",
);

const GetSchoolAdminsUseCase = require(
  "../../../application/school_admins/use_cases/get_school_admins",
);

const RegisterSchoolAdminUseCase = require(
  "../../../application/school_admins/use_cases/register_school_admin",
);


// Repository
const schoolAdminRepository =
  new SchoolAdminRepositoryImpl();


// Use cases
const getSchoolAdminsUseCase =
  new GetSchoolAdminsUseCase(
    schoolAdminRepository,
  );

const registerSchoolAdminUseCase =
  new RegisterSchoolAdminUseCase(
    schoolAdminRepository,
  );


// Export
module.exports = {
  schoolAdminRepository,

  getSchoolAdminsUseCase,
  registerSchoolAdminUseCase,
};