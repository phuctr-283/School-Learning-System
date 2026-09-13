from apps.administrators.application.dto.school_admin.school_admin_dto import (
    SchoolAdminDTO,
)


class GetSchoolAdminsUseCase:

    def __init__(self, school_admin_repository):
        self.school_admin_repository = school_admin_repository

    def execute(self):

        admins = self.school_admin_repository.get_all()

        return [
            SchoolAdminDTO(
                school_admin_id=admin.school_admin_id,
                full_name=admin.full_name,
                gender=admin.gender,
                email=admin.email,
                phone=admin.phone,
                university_id=admin.university_id,
                university_name=admin.university_name,
                status=admin.status,
            )
            for admin in admins
        ]