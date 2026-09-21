from decimal import Decimal

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

from apps.class_sections.infrastructure.persistence.models.class_section_model import (
    ClassSectionModel,
)

from apps.assignments.application.dto.assignment_list_dto import (
    AssignmentListDTO,
)
from apps.assignments.application.dto.assignment_content_dto import AssignmentContentDTO


class MongoAssignmentRepository(
    AssignmentRepository,
):

    def _get_teacher_by_email(
        self,
        university,
        teacher_email: str,
    ):
        normalized_email = (teacher_email or "").strip().lower()

        if not normalized_email:
            return None

        departments = list(
            DepartmentModel.objects(
                university=university,
                is_active=True,
            )
        )

        if not departments:
            return None

        return TeacherModel.objects(
            email=normalized_email,
            department__in=departments,
            status="active",
        ).first()

    def create_by_teacher_email(
        self,
        assignment: Assignment,
        teacher_email: str,
    ) -> Assignment:

        university = UniversityModel.objects(
            university_id=assignment.university_id,
            is_active=True,
        ).first()

        if university is None:
            raise ValueError(
                "Không tìm thấy trường đại học.",
            )

        subject = SubjectModel.objects(
            university=university,
            subject_id=assignment.subject_id,
        ).first()

        if subject is None:
            raise ValueError(
                "Không tìm thấy môn học thuộc trường đại học.",
            )

        if subject.department is None:
            raise ValueError(
                "Môn học chưa được gán khoa.",
            )

        subject_department_id = str(
            subject.department.department_id,
        )

        if str(assignment.department_id) != subject_department_id:
            raise ValueError(
                "Khoa của bài tập không khớp với khoa của môn học.",
            )

        department = DepartmentModel.objects(
            department_id=subject_department_id,
            university=university,
            is_active=True,
        ).first()

        if department is None:
            raise ValueError(
                "Không tìm thấy khoa thuộc trường đại học.",
            )

        normalized_email = (teacher_email or "").strip().lower()

        if not normalized_email:
            raise ValueError(
                "Không xác định được email giảng viên.",
            )

        teacher = TeacherModel.objects(
            email=normalized_email,
            department=department,
            status="active",
        ).first()

        if teacher is None:
            raise ValueError(
                "Giảng viên không thuộc khoa của môn học " "hoặc không tồn tại.",
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
            is_active=True,
        ).first()

        if university is None:
            return None

        assignment_model = (
            AssignmentModel.objects(
                assignment_id=assignment_id,
                university=university,
                is_active=True,
            )
            .select_related()
            .first()
        )

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
            is_active=True,
        ).first()

        if university is None:
            return []

        if department_id:
            department = DepartmentModel.objects(
                department_id=department_id,
                university=university,
                is_active=True,
            ).first()

            if department is None:
                return []

            teacher = TeacherModel.objects(
                teacher_id=teacher_id,
                department=department,
                status="active",
            ).first()

        else:
            departments = list(
                DepartmentModel.objects(
                    university=university,
                    is_active=True,
                )
            )

            if not departments:
                return []

            teacher = TeacherModel.objects(
                teacher_id=teacher_id,
                department__in=departments,
                status="active",
            ).first()

        if teacher is None:
            return []

        assignments = (
            AssignmentModel.objects(
                teacher=teacher,
                university=university,
                is_active=True,
            )
            .order_by("-created_at")
            .select_related()
        )

        return [AssignmentMapper.to_entity(assignment) for assignment in assignments]

    def get_by_class_section_id(
        self,
        class_section_id: str,
    ):
        class_section = ClassSectionModel.objects(
            class_section_id=class_section_id,
        ).first()

        if not class_section:
            return []

        assignments = AssignmentModel.objects(
            class_section=class_section,
            is_active=True,
        ).select_related()

        result = []

        for assignment in assignments:
            lesson = assignment.lesson

            if not lesson:
                continue

            result.append(
                {
                    "assignment_id": str(
                        assignment.assignment_id,
                    ),
                    "class_section_id": str(
                        class_section.class_section_id,
                    ),
                    "lesson_id": str(
                        lesson.lesson_id,
                    ),
                    "lesson_number": lesson.lesson_number,
                    "title": assignment.title,
                    "description": (assignment.description or ""),
                    "assignment_kind": (assignment.assignment_kind),
                    "exam_type": assignment.exam_type,
                }
            )

        result.sort(
            key=lambda item: (
                item["lesson_number"],
                item["assignment_kind"],
                item["title"],
            )
        )

        return result

    def _get_university(
        self,
        university_id: str,
    ):
        return UniversityModel.objects(
            university_id=university_id,
            is_active=True,
        ).first()

    def _to_assignment_list_dto(
        self,
        assignment: AssignmentModel,
    ) -> AssignmentListDTO:

        return AssignmentListDTO(
            assignment_id=assignment.assignment_id,
            subject_name=assignment.subject.name,
            title=assignment.title,
            description=assignment.description,
            assignment_type=str(
                assignment.assignment_type,
            ),
            total_score=Decimal(
                str(assignment.total_score),
            ),
            status=str(assignment.status),
            is_active=assignment.is_active,
            created_at=assignment.created_at,
        )

    def get_assignments(
        self,
        university_id: str,
        teacher_email: str,
    ) -> list[AssignmentListDTO]:

        university = self._get_university(
            university_id,
        )

        if university is None:
            return []

        teacher = self._get_teacher_by_email(
            university=university,
            teacher_email=teacher_email,
        )

        if teacher is None:
            return []

        assignments = (
            AssignmentModel.objects(
                university=university,
                teacher=teacher,
                is_active=True,
            )
            .order_by("-created_at")
            .select_related()
        )

        return [
            self._to_assignment_list_dto(
                assignment,
            )
            for assignment in assignments
        ]

    def get_assignments_by_subject(
        self,
        university_id: str,
        teacher_email: str,
        subject_id: str,
    ) -> list[AssignmentListDTO]:

        university = self._get_university(
            university_id,
        )

        if university is None:
            return []

        teacher = self._get_teacher_by_email(
            university=university,
            teacher_email=teacher_email,
        )

        if teacher is None:
            return []

        subject = SubjectModel.objects(
            subject_id=subject_id,
            university=university,
        ).first()

        if subject is None:
            return []

        assignments = (
            AssignmentModel.objects(
                university=university,
                teacher=teacher,
                subject=subject,
                is_active=True,
            )
            .order_by("-created_at")
            .select_related()
        )

        return [
            self._to_assignment_list_dto(
                assignment,
            )
            for assignment in assignments
        ]

    def get_content_by_id(
        self,
        assignment_id: str,
        university_id: str,
        teacher_email: str,
    ) -> AssignmentContentDTO | None:

        university = UniversityModel.objects(
            university_id=university_id,
            is_active=True,
        ).first()

        if university is None:
            return None

        teacher = self._get_teacher_by_email(
            university=university,
            teacher_email=teacher_email,
        )

        if teacher is None:
            return None

        assignment = (
            AssignmentModel.objects(
                assignment_id=assignment_id,
                university=university,
                teacher=teacher,
                is_active=True,
            )
            .only(
                "assignment_id",
                "title",
                "description",
                "university",
                "subject",
                "teacher",
                "assignment_type",
                "total_score",
                "duration_minutes",
                "status",
                "is_active",
                "created_at",
                "updated_at",
            ).first()
            
        )

        if assignment is None:
            return None

        return AssignmentMapper.to_content_dto(
            assignment,
        )
