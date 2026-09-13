const DepartmentRepositoryImpl = require("../../../infrastructure/repositories/department/department_repository_impl");

const GetActivesDepartmentsUseCase = require("../../../application/departments/use_cases/get_actives_departments");

const GetActiveDepartmentsUseCase = require("../../../application/departments/use_cases/get_active_departments");

const GetUniversityDepartmentsUseCase = require("../../../application/departments/use_cases/get_university_departments");

const CreateDepartmentUseCase = require("../../../application/departments/use_cases/create_department");

const departmentRepository = new DepartmentRepositoryImpl();

const getActivesDepartmentsUseCase = new GetActivesDepartmentsUseCase(
  departmentRepository,
);
const getActiveDepartmentsUseCase = new GetActiveDepartmentsUseCase(
  departmentRepository,
);

const getUniversityDepartmentsUseCase = new GetUniversityDepartmentsUseCase(
  departmentRepository,
);

const createDepartmentUseCase = new CreateDepartmentUseCase(
  departmentRepository,
);
module.exports = {
  departmentRepository,

  getActiveDepartmentsUseCase,
  getUniversityDepartmentsUseCase,
  createDepartmentUseCase,
  getActivesDepartmentsUseCase,
};
