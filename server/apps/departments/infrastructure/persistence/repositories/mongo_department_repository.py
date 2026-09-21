from apps.departments.domain.entities.department_entity import (
    Department,
)

from apps.departments.domain.repositories.department_repository import (
    DepartmentRepository,
)

from apps.departments.infrastructure.persistence.models.department_model import (
    DepartmentModel,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)

from apps.teachers.infrastructure.persistence.models.teacher_model import (
    TeacherModel,
)


class MongoDepartmentRepository(
    DepartmentRepository,
):

    def get_by_university(
        self,
        university_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if university is None:
            return []

        departments = (
            DepartmentModel.objects(
                university=university,
            )
            .order_by("department_number")
            .select_related()
        )

        result = []

        for model in departments:

            head = model.head

            result.append(
                Department(
                    department_id=model.department_id,
                    department_number=model.department_number,
                    name=model.name,
                    university_id=university.university_id,
                    university_name=university.name,
                    head_id=(head.teacher_id if head else None),
                    head_name=(head.full_name if head else None),
                    is_active=model.is_active,
                )
            )

        return result

    def find_by_id(
        self,
        department_id: str,
        university_id: str,
    ):

        return self.get_by_id(
            department_id=department_id,
            university_id=university_id,
        )

    def get_by_id(
        self,
        department_id: str,
        university_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if university is None:
            return None

        return DepartmentModel.objects(
            department_id=department_id,
            university=university,
        ).first()

    def exists_department_number(
        self,
        university_id: str,
        department_number: str,
    ) -> bool:

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if university is None:
            return False

        return (
            DepartmentModel.objects(
                university=university,
                department_number=department_number,
            ).first()
            is not None
        )

    def create(
        self,
        entity: Department,
    ):

        university = UniversityModel.objects(
            university_id=entity.university_id,
        ).first()

        if university is None:
            raise ValueError("Không tìm thấy trường đại học.")

        head = None

        if entity.head_id:

            if not entity.head_department_id:
                raise ValueError("Cần có khoa của trưởng khoa.")

            head_department = DepartmentModel.objects(
                department_id=entity.head_department_id,
                university=university,
            ).first()

            if head_department is None:
                raise ValueError("Không tìm thấy khoa của trưởng khoa.")

            head = TeacherModel.objects(
                teacher_id=entity.head_id,
                department=head_department,
            ).first()

            if head is None:
                raise ValueError("Không tìm thấy trưởng khoa.")

        model = DepartmentModel(
            department_id=entity.department_id,
            department_number=entity.department_number,
            name=entity.name,
            university=university,
            head=head,
            is_active=entity.is_active,
        )

        model.save()

        return entity

    def get_active_by_university(
        self,
        university_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
            is_active=True,
        ).first()

        if university is None:
            return []

        return list(
            DepartmentModel.objects(
                university=university,
                is_active=True,
            ).order_by("department_number")
        )

    def get_active_by_university_authenticated(
        self,
        university_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if university is None:
            return []

        departments = (
            DepartmentModel.objects(
                university=university,
                is_active=True,
            )
            .order_by("department_number")
            .select_related()
        )

        return [
            Department(
                department_id=department.department_id,
                department_number=department.department_number,
                name=department.name,
                university_id=university.university_id,
                university_name=university.name,
                head_id=(department.head.teacher_id if department.head else None),
                head_name=(department.head.full_name if department.head else None),
                is_active=department.is_active,
            )
            for department in departments
        ]
    @staticmethod
    def _normalize_department_number(value: str) -> str:
        value = str(value).strip()

        if not value:
            return ""

        return value.lstrip("0") or "0"

    def find_by_number(
        self,
        university_id: str,
        department_number: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if university is None:
            return None

        normalized_number = (
            self._normalize_department_number(
                department_number
            )
        )

        departments = DepartmentModel.objects(
            university=university,
        )

        for department in departments:

            db_number = (
                self._normalize_department_number(
                    department.department_number
                )
            )

            if db_number == normalized_number:
                return department

        return None