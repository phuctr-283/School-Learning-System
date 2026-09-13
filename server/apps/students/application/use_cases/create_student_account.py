from apps.users.application.dto.user_dto import (
    CreateUserDTO,
)

from apps.users.domain.enums.account_level import (
    AccountLevel,
)


class CreateStudentAccountUseCase:

    def __init__(
        self,
        create_user_use_case,
    ):
        self.create_user_use_case = create_user_use_case

    def execute(
        self,
        student_id: str,
        university_id: str,
    ):

        student_id = student_id.strip().upper()

        data = CreateUserDTO(
            user_id=None,
            username=student_id,
            password=student_id,
            account_level=(AccountLevel.STUDENT),
            university_id=university_id,
        )

        return self.create_user_use_case.execute(data)
