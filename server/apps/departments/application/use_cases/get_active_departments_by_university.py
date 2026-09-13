class GetActiveDepartmentsByUniversityUseCase:

    def __init__(
        self,
        department_repository,
        university_repository,
    ):

        self.department_repository = (
            department_repository
        )

        self.university_repository = (
            university_repository
        )

    def execute(self, university_id):

        if not university_id:
            raise ValueError(
                "Không xác định được trường đại học"
            )

        university = (
            self.university_repository.find_by_id(
                university_id
            )
        )

        if not university:
            raise ValueError(
                "Không tìm thấy trường đại học"
            )

        return (
            self.department_repository
            .get_active_by_university(
                university_id
            )
        )