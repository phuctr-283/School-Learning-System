const StudentAssignmentRepositoryImpl = require(
  "../../repositories/assignment/student_assignment_repository_impl"
);
const GetStudentAssignmentUseCase = require(
  "../../../application/assignments/use_cases/get_student_assignment"
);

const SaveStudentAssignmentUseCase = require(
  "../../../application/assignments/use_cases/save_student_assignment"
);

const SubmitStudentAssignmentUseCase = require(
  "../../../application/assignments/use_cases/submit_student_assignment"
);
const assignmentRepository =
  new StudentAssignmentRepositoryImpl();

const getStudentAssignmentUseCase =
  new GetStudentAssignmentUseCase(
    assignmentRepository
  );

const saveStudentAssignmentUseCase =
  new SaveStudentAssignmentUseCase(
    assignmentRepository
  );

const submitStudentAssignmentUseCase =
  new SubmitStudentAssignmentUseCase(
    assignmentRepository
  );

module.exports = {
  getStudentAssignmentUseCase,
  saveStudentAssignmentUseCase,
  submitStudentAssignmentUseCase,
};