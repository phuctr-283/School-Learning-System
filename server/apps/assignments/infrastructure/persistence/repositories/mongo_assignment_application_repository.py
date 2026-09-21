from datetime import datetime, timezone


def ensure_aware_datetime(value):
    if value is None:
        return None

    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)

    return value.astimezone(timezone.utc)


from apps.assignments.domain.repositories.assignment_application_repository import (
    AssignmentApplicationRepository,
)

from apps.assignments.application.dto.assignment_application_dto import (
    AssignmentApplicationDTO,
)

from apps.assignments.infrastructure.persistence.models.assignment_application_model import (
    AssignmentApplicationModel,
)
from apps.assignments.infrastructure.persistence.mappers.assignment_application_mapper import (
    AssignmentApplicationMapper,
)
from apps.assignments.infrastructure.persistence.models.assignment_application_class_section_model import (
    AssignmentApplicationClassSectionModel,
)
from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)
from apps.assignments.infrastructure.persistence.models.assignment_model import (
    AssignmentModel,
)

from apps.teachers.infrastructure.persistence.models.teacher_model import (
    TeacherModel,
)

from apps.class_sections.infrastructure.persistence.models.class_section_model import (
    ClassSectionModel,
)

from apps.lessons.infrastructure.persistence.models.class_section_lesson_plan_model import (
    ClassSectionLessonPlanModel,
)
from apps.students.infrastructure.persistence.models.student_model import StudentModel
from apps.class_sections.infrastructure.persistence.models.class_section_student_model import (
    ClassSectionStudentModel,
)
from apps.assignments.infrastructure.persistence.models.assignment_attempt_answer_model import (
    AssignmentAttemptAnswerModel,
)
from apps.assignments.infrastructure.persistence.models.assignment_attempt_model import (
    AssignmentAttemptModel,
)


class MongoAssignmentApplicationRepository(AssignmentApplicationRepository):

    def __init__(
        self,
        assignment_application_id_generator,
    ):
        self.assignment_application_id_generator = assignment_application_id_generator

    def apply_to_class_sections(
        self,
        assignment_id: str,
        lesson_id: str,
        class_section_ids: list[str],
        teacher_email: str,
        max_attempts: int = 1,
    ):

        teacher = TeacherModel.objects(
            email=teacher_email,
            status="active",
        ).first()

        if teacher is None:
            raise ValueError("Không tìm thấy giáo viên tương ứng với tài khoản.")

        if teacher.department is None:
            raise ValueError("Giáo viên chưa thuộc khoa.")

        department = teacher.department

        if department.university is None:
            raise ValueError("Khoa của giáo viên chưa thuộc trường đại học.")

        university = department.university

        university_id = str(university.university_id)

        assignment = AssignmentModel.objects(
            assignment_id=assignment_id,
            teacher=teacher,
            university=university_id,
            is_active=True,
        ).first()

        if assignment is None:
            raise ValueError(
                "Không tìm thấy bài tập hoặc bài tập không thuộc giáo viên."
            )

        if assignment.teacher != teacher:
            raise ValueError("Bài tập không thuộc giáo viên hiện tại.")

        if assignment.subject is None:
            raise ValueError("Bài tập chưa có môn học.")

        subject = assignment.subject

        if subject.department != department:
            raise ValueError("Môn học của bài tập không thuộc khoa của giáo viên.")

        if subject.university is None:
            raise ValueError("Môn học của bài tập chưa thuộc trường đại học.")

        if str(subject.university.university_id) != university_id:
            raise ValueError(
                "Môn học của bài tập không thuộc trường đại học của giáo viên."
            )

        class_sections = list(
            ClassSectionModel.objects(
                class_section_id__in=class_section_ids,
                subject=subject,
                teacher=teacher,
                status__in=[
                    "active",
                    "planned",
                ],
            ).select_related()
        )

        class_section_map = {
            str(class_section.class_section_id): class_section
            for class_section in class_sections
        }

        missing_class_sections = [
            class_section_id
            for class_section_id in class_section_ids
            if class_section_id not in class_section_map
        ]

        if missing_class_sections:
            raise ValueError(
                "Không tìm thấy các nhóm lớp học phần "
                "thuộc môn học và giáo viên hiện tại: "
                + ", ".join(missing_class_sections)
            )

        for class_section in class_sections:

            if class_section.subject != subject:
                raise ValueError(
                    f"Nhóm lớp học phần "
                    f"{class_section.class_section_id} "
                    f"không thuộc môn học của bài tập."
                )

            if class_section.teacher != teacher:
                raise ValueError(
                    f"Nhóm lớp học phần "
                    f"{class_section.class_section_id} "
                    f"không thuộc giáo viên hiện tại."
                )

        for class_section in class_sections:

            lesson_plan = ClassSectionLessonPlanModel.objects(
                class_section=class_section,
            ).first()

            if lesson_plan is None:
                raise ValueError(
                    f"Nhóm lớp học phần "
                    f"{class_section.class_section_id} "
                    f"chưa có kế hoạch buổi học."
                )

            lesson_opening = None

            for opening in lesson_plan.lesson_openings or []:

                if str(opening.lesson.lesson_id) == str(lesson_id):
                    lesson_opening = opening
                    break

            if lesson_opening is None:
                raise ValueError(
                    f"Buổi học {lesson_id} "
                    f"không tồn tại trong nhóm "
                    f"{class_section.class_section_id}."
                )

        now = datetime.now(timezone.utc)

        application = AssignmentApplicationModel.objects(
            assignment=assignment,
            lesson_id=lesson_id,
        ).first()

        if application is None:

            application = AssignmentApplicationModel(
                assignment_application_id=(
                    self.assignment_application_id_generator.generate()
                ),
                university=university,
                assignment=assignment,
                class_sections=[
                    AssignmentApplicationClassSectionModel(
                        class_section=class_section,
                        status="closed",
                        opened_at=now,
                        closed_at=None,
                    )
                    for class_section in class_sections
                ],
                lesson_id=lesson_id,
                status="published",
                open_at=now,
                due_at=None,
                max_attempts=max_attempts,
                created_at=now,
                updated_at=now,
            )

        else:

            existing_items = {
                str(item.class_section.class_section_id): item
                for item in application.class_sections
            }

            new_class_sections = []

            for class_section in class_sections:

                class_section_id = str(class_section.class_section_id)

                existing_item = existing_items.get(class_section_id)

                if existing_item:

                    new_class_sections.append(existing_item)

                else:

                    new_class_sections.append(
                        AssignmentApplicationClassSectionModel(
                            class_section=class_section,
                            status="closed",
                            opened_at=now,
                            closed_at=None,
                        )
                    )

            application.class_sections = new_class_sections

            application.status = "published"

            application.open_at = application.open_at or now

            application.max_attempts = max_attempts

            application.updated_at = now

        application.save()

        return AssignmentApplicationDTO(
            assignment_application_id=(application.assignment_application_id),
            assignment_id=str(assignment.assignment_id),
            class_section_ids=[
                str(item.class_section.class_section_id)
                for item in application.class_sections
                if item.class_section is not None
            ],
            lesson_id=application.lesson_id,
            status=application.status,
            open_at=application.open_at,
            due_at=application.due_at,
            max_attempts=application.max_attempts,
        )

    def get_by_id(
        self,
        assignment_application_id: str,
        university_id: str,
    ):

        application = AssignmentApplicationModel.objects(
            assignment_application_id=(assignment_application_id),
        ).first()

        if application is None:
            return None

        if application.university is None:
            return None

        if str(application.university.university_id) != str(university_id):
            return None

        return AssignmentApplicationDTO(
            assignment_application_id=(application.assignment_application_id),
            assignment_id=str(application.assignment.assignment_id),
            class_section_ids=[
                str(class_section.class_section_id)
                for class_section in (application.class_sections)
            ],
            lesson_id=application.lesson_id,
            status=application.status,
            open_at=application.open_at,
            due_at=application.due_at,
            max_attempts=application.max_attempts,
        )

    def get_by_class_section_and_lesson(
        self,
        class_section_id: str,
        lesson_id: str,
        teacher_email: str,
    ):

        if not class_section_id:
            raise ValueError("Mã lớp học phần không được để trống.")

        if not lesson_id:
            raise ValueError("Mã lesson không được để trống.")

        if not teacher_email:
            raise ValueError("Không xác định được email tài khoản giáo viên.")

        teacher = TeacherModel.objects(
            email=teacher_email.strip().lower(),
            status="active",
        ).first()

        if teacher is None:
            raise ValueError("Không tìm thấy giáo viên tương ứng với tài khoản.")

        department = teacher.department

        if department is None:
            raise ValueError("Giáo viên chưa thuộc khoa.")

        university = department.university

        if university is None:
            raise ValueError("Khoa của giáo viên chưa thuộc trường đại học.")

        class_section = ClassSectionModel.objects(
            class_section_id=class_section_id,
            teacher=teacher,
        ).first()

        if class_section is None:
            raise ValueError("Không tìm thấy lớp học phần thuộc giáo viên hiện tại.")

        applications = (
            AssignmentApplicationModel.objects(
                university=university,
                class_sections__class_section=class_section,
                lesson_id=lesson_id,
                status="published",
            )
            .order_by("-created_at")
            .select_related()
        )

        result = []

        for application in applications:

            target = next(
                (
                    item
                    for item in application.class_sections
                    if item.class_section == class_section
                ),
                None,
            )

            if target is None:
                continue

            if target.status != "active":
                continue

            result.append(AssignmentApplicationMapper.to_content_dto(application))

        return result

    def update_class_section_status(
        self,
        assignment_application_id: str,
        class_section_id: str,
        teacher_email: str,
        status: str,
    ):

        teacher = TeacherModel.objects(
            email=teacher_email.strip().lower(),
            status="active",
        ).first()

        if teacher is None:
            raise ValueError("Không tìm thấy giáo viên.")

        department = teacher.department

        if department is None:
            raise ValueError("Giáo viên chưa thuộc khoa.")

        university = department.university

        if university is None:
            raise ValueError("Khoa chưa thuộc trường đại học.")

        application = AssignmentApplicationModel.objects(
            assignment_application_id=(assignment_application_id),
            university=university,
        ).first()

        if application is None:
            raise ValueError("Không tìm thấy bài áp dụng.")

        assignment = application.assignment

        if assignment is None:
            raise ValueError("Bài tập không tồn tại.")

        if assignment.teacher != teacher:
            raise ValueError("Bài tập không thuộc giáo viên hiện tại.")

        class_section = ClassSectionModel.objects(
            class_section_id=class_section_id,
            teacher=teacher,
        ).first()
        if (
            class_section.teacher is None
            or class_section.teacher.department is None
            or class_section.teacher.department.university != university
        ):
            raise ValueError("Lớp học phần không thuộc trường đại học hiện tại.")
        target = None

        for item in application.class_sections:

            if item.class_section == class_section:
                target = item
                break

        if target is None:
            raise ValueError("Bài tập chưa được áp dụng cho lớp học phần này.")

        now = datetime.now(timezone.utc)

        target.status = status

        if status == "active":

            target.opened_at = now
            target.closed_at = None

        else:

            target.closed_at = now

        application.updated_at = now

        application.save()

        return AssignmentApplicationMapper.to_content_dto(application)

    def verify_student_assignment_qr(
        self,
        student_id: str,
        assignment_application_id: str,
        class_section_id: str,
        lesson_id: str,
    ):

        student_id = str(student_id or "").strip()
        assignment_application_id = str(assignment_application_id or "").strip()
        class_section_id = str(class_section_id or "").strip()
        lesson_id = str(lesson_id or "").strip()

        if not student_id:
            raise ValueError("Mã sinh viên không được để trống.")

        if not assignment_application_id:
            raise ValueError("Thiếu mã bài tập.")

        if not class_section_id:
            raise ValueError("Thiếu mã lớp học phần.")

        if not lesson_id:
            raise ValueError("Thiếu mã bài học.")

        application = (
            AssignmentApplicationModel.objects(
                assignment_application_id=assignment_application_id,
            )
            .first()
            .select_related()
        )

        if not application:
            raise ValueError("Không tìm thấy bài tập.")

        if application.status != "published":
            raise ValueError("Bài tập hiện không khả dụng.")

        if str(application.lesson_id) != lesson_id:
            raise ValueError("Bài tập không thuộc bài học này.")

        class_section = (
            ClassSectionModel.objects(
                class_section_id=class_section_id,
            )
            .first()
            .select_related()
        )

        if not class_section:
            raise ValueError("Không tìm thấy lớp học phần.")

        if class_section.status != "active":
            raise ValueError("Lớp học phần hiện không hoạt động.")

        class_section_state = next(
            (
                item
                for item in (application.class_sections or [])
                if item.class_section
                and str(item.class_section.class_section_id) == class_section_id
            ),
            None,
        )

        if not class_section_state:
            raise ValueError("Bài tập không được áp dụng cho lớp học phần này.")

        if class_section_state.status != "active":
            raise ValueError("Bài tập hiện chưa được mở cho lớp học phần này.")

        student = (
            StudentModel.objects(
                student_id=student_id,
            )
            .first()
            .select_related()
        )

        if not student:
            raise ValueError("Mã sinh viên không tồn tại.")

        enrollment = ClassSectionStudentModel.objects(
            student=student,
            class_section=class_section,
        ).first()

        if not enrollment:
            raise ValueError("Sinh viên không thuộc lớp học phần này.")

        # --------------------------------------------------
        # 8. Kiểm tra lesson opening
        # --------------------------------------------------

        lesson_plan = (
            ClassSectionLessonPlanModel.objects(
                class_section=class_section,
            )
            .first()
            .select_related()
        )

        if not lesson_plan:
            raise ValueError("Không tìm thấy kế hoạch bài học của lớp.")

        lesson_opening = next(
            (
                opening
                for opening in (lesson_plan.lesson_openings or [])
                if opening.lesson and str(opening.lesson.lesson_id) == lesson_id
            ),
            None,
        )

        if not lesson_opening:
            raise ValueError("Không tìm thấy bài học.")

        if lesson_opening.status != "open":
            raise ValueError("Bài học hiện chưa được mở.")

        # --------------------------------------------------
        # 9. open_at / due_at
        # --------------------------------------------------

        now = datetime.now(timezone.utc)

        open_at = ensure_aware_datetime(application.open_at)

        due_at = ensure_aware_datetime(application.due_at)

        if open_at and now < open_at:
            raise ValueError("Bài tập chưa đến thời gian mở.")

        if due_at and now > due_at:
            raise ValueError("Bài tập đã hết hạn.")

        return {
            "assignment_application_id": (application.assignment_application_id),
            "class_section_id": (class_section.class_section_id),
            "lesson_id": application.lesson_id,
            "student_id": student.student_id,
        }
