from apps.assignments.domain.repositories.assignment_repository import (
    AssignmentRepository,
)

from apps.assignments.domain.entities.assignment_entity import (
    Assignment,
)

from apps.assignments.infrastructure.persistence.models.assignment_model import (
    AssignmentModel,
)

from apps.assignments.infrastructure.persistence.mappers.assignment_mapper import (
    AssignmentMapper,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)

from apps.subjects.infrastructure.persistence.models.subject_model import (
    SubjectModel,
)

from apps.teachers.infrastructure.persistence.models.teacher_model import (
    TeacherModel,
)

from apps.departments.infrastructure.persistence.models.department_model import (
    DepartmentModel,
)


class MongoAssignmentRepository(
    AssignmentRepository,
):

    def create(
        self,
        assignment: Assignment,
    ) -> Assignment:

        university = UniversityModel.objects(
            university_id=assignment.university_id,
        ).first()

        if university is None:
            raise ValueError(
                "Không tìm thấy trường đại học.",
            )

        department = DepartmentModel.objects(
            department_id=assignment.department_id,
            university=university,
        ).first()

        if department is None:
            raise ValueError(
                "Không tìm thấy khoa.",
            )

        subject = SubjectModel.objects(
            subject_id=assignment.subject_id,
            university=university,
        ).first()

        if subject is None:
            raise ValueError(
                "Không tìm thấy môn học.",
            )

        teacher = TeacherModel.objects(
            teacher_id=assignment.teacher_id,
            department=department,
        ).first()

        if teacher is None:
            raise ValueError(
                "Không tìm thấy giảng viên.",
            )

        assignment_model = AssignmentMapper.to_model(
            entity=assignment,
            university=university,
            subject=subject,
            teacher=teacher,
        )

        assignment_model.save()

        return assignment

    def get_by_id(
        self,
        assignment_id: str,
        university_id: str,
    ) -> Assignment | None:

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if university is None:
            return None

        assignment_model = AssignmentModel.objects(
            assignment_id=assignment_id,
            university=university,
            is_active=True,
        ).first()

        if assignment_model is None:
            return None

        return AssignmentMapper.to_entity(
            assignment_model,
        )

    def get_by_teacher(
        self,
        teacher_id: str,
        university_id: str,
        department_id: str | None = None,
    ) -> list[Assignment]:

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if university is None:
            return []

        teacher_query = {
            "teacher_id": teacher_id,
            "department__university": university,
        }

        if department_id:
            teacher_query[
                "department__department_id"
            ] = department_id

        teacher = TeacherModel.objects(
            **teacher_query,
        ).first()

        if teacher is None:
            return []

        assignment_models = (
            AssignmentModel.objects(
                teacher=teacher,
                university=university,
                is_active=True,
            )
            .order_by("-created_at")
        )

        return [
            AssignmentMapper.to_entity(model)
            for model in assignment_models
        ]