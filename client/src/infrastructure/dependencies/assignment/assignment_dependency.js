const AssignmentRepositoryImpl = require("../../repositories/assignment/assignment_repository_impl");
const AssignmentApplicationRepositoryImpl = require("../../repositories/assignment/assignment_application_repository_impl");
const CreateAssignmentUseCase = require("../../../application/assignments/use_cases/create_assignment.use_case");

const GetAssignmentsUseCase = require("../../../application/assignments/use_cases/get_assignments.use_case");
const GetAssignmentsBySubjectUseCase = require("../../../application/assignments/use_cases/get_assignments_by_subject.use_case");
const GetAssignmentUseCase = require("../../../application/assignments/use_cases/get_assignment_use_case");
const ApplyAssignmentUseCase = require("../../../application/assignments/use_cases/apply_assignment.use_case");
const GetAssignmentApplicationsUseCase = require("../../../application/assignments/use_cases/get_assignment_applications_use_case");
const UpdateAssignmentApplicationClassSectionStatusUseCase = require("../../../application/assignments/use_cases/update_assignment_application_class_section_status.use_case");
const VerifyStudentAssignmentQrUseCase = require("../../../application/assignments/use_cases/verify_student_assignment_qr");
const GetStudentAssignmentUseCase = require("../../../application/assignments/use_cases/get_student_assignment");
const assignmentRepositoryImpl = new AssignmentRepositoryImpl();
const assignmentApplicationRepositoryImpl =
  new AssignmentApplicationRepositoryImpl();
const createAssignmentUseCase = new CreateAssignmentUseCase(
  assignmentRepositoryImpl,
);

const getAssignmentsUseCase = new GetAssignmentsUseCase(
  assignmentRepositoryImpl,
);
const getAssignmentsBySubjectUseCase = new GetAssignmentsBySubjectUseCase(
  assignmentRepositoryImpl,
);
const getAssignmentUseCase = new GetAssignmentUseCase(assignmentRepositoryImpl);
const applyAssignmentUseCase = new ApplyAssignmentUseCase(
  assignmentApplicationRepositoryImpl,
);
const getAssignmentApplicationsUseCase = new GetAssignmentApplicationsUseCase(
  assignmentApplicationRepositoryImpl,
);
const updateAssignmentApplicationClassSectionStatusUseCase =
  new UpdateAssignmentApplicationClassSectionStatusUseCase(
    assignmentApplicationRepositoryImpl,
  );

const verifyStudentAssignmentQrUseCase = new VerifyStudentAssignmentQrUseCase(
  assignmentApplicationRepositoryImpl,
);
const getStudentAssignmentUseCase = new GetStudentAssignmentUseCase(
  assignmentApplicationRepositoryImpl,
);
module.exports = {
  getAssignmentsUseCase,
  createAssignmentUseCase,
  getAssignmentsBySubjectUseCase,
  getAssignmentUseCase,
  applyAssignmentUseCase,
  getAssignmentApplicationsUseCase,
  updateAssignmentApplicationClassSectionStatusUseCase,
  verifyStudentAssignmentQrUseCase,
  getStudentAssignmentUseCase,
};
