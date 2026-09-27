from apps.assignments.application.exceptions.assignment_exceptions import AssignmentBadRequestError
class GetStudentAssignmentHistoryUseCase:

    def __init__(
        self,
        student_assignment_repository,
    ):
        self.student_assignment_repository = student_assignment_repository

    def execute(
        self,
        assignment_application_id,
        student_id,
        class_section_id,
    ):
        assignment_application_id = str(assignment_application_id).strip()

        student_id = str(student_id).strip().upper()

        class_section_id = str(class_section_id).strip()

        if not assignment_application_id:
            raise AssignmentBadRequestError("Thiếu mã áp dụng bài tập.")

        if not student_id:
            raise AssignmentBadRequestError("Thiếu mã sinh viên.")

        if not class_section_id:
            raise AssignmentBadRequestError("Thiếu mã lớp học phần.")

        return self.student_assignment_repository.get_attempt_history(
            assignment_application_id=(assignment_application_id),
            student_id=student_id,
            class_section_id=class_section_id,
        )
