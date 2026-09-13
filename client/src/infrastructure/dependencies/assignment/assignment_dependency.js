const AssignmentRepositoryImpl = require("../../repositories/assignment/assignment_repository_impl");

const CreateAssignmentUseCase = require("../../../application/assignments/use_cases/create_assignment.use_case");

const GetAssignmentsUseCase = require("../../../application/assignments/use_cases/get_assignments.use_case");

const assignmentRepositoryImpl = new AssignmentRepositoryImpl();

const createAssignmentUseCase = new CreateAssignmentUseCase(
  assignmentRepositoryImpl,
);

const getAssignmentsUseCase = new GetAssignmentsUseCase(
  assignmentRepositoryImpl,
);
module.exports = {
    getAssignmentsUseCase,
    createAssignmentUseCase,
};
