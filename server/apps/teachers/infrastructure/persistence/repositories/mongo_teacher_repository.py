from apps.teachers.domain.entities.teacher_entity import (
    Teacher,
)

from apps.teachers.domain.repositories.teacher_repository import (
    TeacherRepository,
)

from apps.teachers.infrastructure.persistence.models.teacher_model import (
    TeacherModel,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)

from apps.departments.infrastructure.persistence.models.department_model import (
    DepartmentModel,
)


class MongoTeacherRepository(
    TeacherRepository,
):

    # =====================================================
    # MODEL -> DOMAIN
    # =====================================================

    @staticmethod
    def _to_entity(
        teacher_model: TeacherModel,
    ) -> Teacher:

        department = teacher_model.department
        university = department.university

        return Teacher(
            teacher_id=teacher_model.teacher_id,
            full_name=teacher_model.full_name,
            gender=teacher_model.gender,
            date_of_birth=teacher_model.date_of_birth,
            email=teacher_model.email,
            phone=teacher_model.phone,
            department_id=department.department_id,
            department_name=department.name,
            university_id=university.university_id,
            university_name=university.name,
            status=teacher_model.status,
        )

    # =====================================================
    # GET BY UNIVERSITY
    # =====================================================

    def get_by_university(
        self,
        university_id: str,
    ) -> list[Teacher]:

        university = UniversityModel.objects(
            university_id=university_id,
            is_active=True,
        ).first()

        if university is None:
            return []

        departments = list(
            DepartmentModel.objects(
                university=university,
                is_active=True,
            )
        )

        if not departments:
            return []

        teacher_models = TeacherModel.objects(
            department__in=departments,
            status="active",
        ).select_related()

        return [self._to_entity(teacher_model) for teacher_model in teacher_models]

    # =====================================================
    # GET BY ID + UNIVERSITY + DEPARTMENT
    # =====================================================

    def get_by_id(
        self,
        teacher_id: str,
        university_id: str,
        department_id: str,
    ) -> Teacher | None:

        university = UniversityModel.objects(
            university_id=university_id,
            is_active=True,
        ).first()

        if university is None:
            return None

        department = DepartmentModel.objects(
            department_id=department_id,
            university=university,
            is_active=True,
        ).first()

        if department is None:
            return None

        teacher_model = (
            TeacherModel.objects(
                teacher_id=teacher_id,
                department=department,
                status="active",
            )
            .select_related()
            .first()
        )

        if teacher_model is None:
            return None

        return self._to_entity(teacher_model)

    # =====================================================
    # FIND BY ID + DEPARTMENT
    # =====================================================

    def find_by_id(
        self,
        teacher_id: str,
        department_id: str,
    ) -> Teacher | None:

        department = DepartmentModel.objects(
            department_id=department_id,
            is_active=True,
        ).first()

        if department is None:
            return None

        teacher_model = (
            TeacherModel.objects(
                teacher_id=teacher_id,
                department=department,
            )
            .select_related()
            .first()
        )

        if teacher_model is None:
            return None

        return self._to_entity(teacher_model)

    # =====================================================
    # EXISTS BY EMAIL
    # =====================================================

    def exists_by_email(
        self,
        email: str,
    ) -> bool:

        return (
            TeacherModel.objects(
                email=email.strip().lower(),
            ).first()
            is not None
        )

    # =====================================================
    # GET BY DEPARTMENT
    # =====================================================

    def get_by_department(
        self,
        department,
    ) -> list[TeacherModel]:

        return list(
            TeacherModel.objects(
                department=department,
            )
        )

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        teacher: Teacher,
        department,
    ) -> Teacher:

        teacher_model = TeacherModel(
            teacher_id=teacher.teacher_id,
            full_name=teacher.full_name,
            gender=teacher.gender,
            date_of_birth=teacher.date_of_birth,
            email=teacher.email,
            phone=teacher.phone,
            department=department,
            status=teacher.status,
        )

        teacher_model.save()

        return teacher

    # =====================================================
    # GET BY NAME
    # =====================================================

    def get_by_name(
        self,
        name: str,
        department_id: str,
        university_id: str,
    ) -> Teacher | None:

        university = UniversityModel.objects(
            university_id=university_id,
            is_active=True,
        ).first()

        if university is None:
            return None

        department = DepartmentModel.objects(
            department_id=department_id,
            university=university,
            is_active=True,
        ).first()

        if department is None:
            return None

        teacher_query = TeacherModel.objects(
            full_name=name.strip(),
            department=department,
            status="active",
        )

        teacher_model = teacher_query.first()

        if teacher_model is None:
            return None

        return self._to_entity(teacher_model)
