from datetime import datetime
from django.utils import timezone

from apps.lessons.domain.entities.lesson_opening_entity import (
    LessonOpening,
)


class EnsureLessonOpeningsUseCase:

    def __init__(
        self,
        class_section_lesson_plan_repository,
        lesson_opening_repository,
        lesson_repository,
        university_repository,
        lesson_opening_id_generator,
    ):

        self.class_section_lesson_plan_repository = class_section_lesson_plan_repository

        self.lesson_opening_repository = lesson_opening_repository

        self.lesson_repository = lesson_repository

        self.university_repository = university_repository

        self.lesson_opening_id_generator = lesson_opening_id_generator

    def execute(
        self,
        university_id: str,
    ):

        # =====================================================
        # UNIVERSITY
        # =====================================================

        university = self.university_repository.find_by_id(
            university_id,
        )

        if not university:
            raise ValueError("Không tìm thấy trường.")

        # =====================================================
        # CLASS SECTION LESSON PLANS
        # =====================================================

        class_section_plans = (
            self.class_section_lesson_plan_repository.get_by_university(
                university_id=university_id,
            )
        )

        created_openings = []

        # =====================================================
        # EACH CLASS SECTION
        # =====================================================

        for class_section_plan in class_section_plans:

            effective_total_lessons = class_section_plan.effective_total_lessons

            if effective_total_lessons is None or effective_total_lessons <= 0:
                raise ValueError(
                    f"Kế hoạch lớp học phần "
                    f"'{class_section_plan.class_section_lesson_plan_id}' "
                    f"chưa có số buổi hợp lệ."
                )

            # =================================================
            # GET LESSON 1 → N
            # =================================================

            lessons = self.lesson_repository.get_by_university_and_lesson_range(
                university_id=university_id,
                total_lessons=effective_total_lessons,
            )

            if len(lessons) < effective_total_lessons:

                raise ValueError(
                    f"Trường chưa có đủ " f"{effective_total_lessons} buổi học chuẩn."
                )

            # =================================================
            # CREATE LESSON OPENING
            # =================================================

            for lesson in lessons:

                exists = self.lesson_opening_repository.exists_by_class_section_plan_and_lesson(
                    university_id=university_id,
                    class_section_lesson_plan_id=(
                        class_section_plan.class_section_lesson_plan_id
                    ),
                    lesson_id=lesson.lesson_id,
                )

                if exists:
                    continue

                lesson_opening_id = self.lesson_opening_id_generator.generate(
                    class_section_lesson_plan_id=(
                        class_section_plan.class_section_lesson_plan_id
                    ),
                    lesson_number=(lesson.lesson_number),
                )

                now = timezone.now()

                entity = LessonOpening(
                    lesson_opening_id=(lesson_opening_id),
                    university_id=(university.university_id),
                    university_name=(university.name),
                    class_section_lesson_plan_id=(
                        class_section_plan.class_section_lesson_plan_id
                    ),
                    lesson_id=(lesson.lesson_id),
                    lesson_number=(lesson.lesson_number),
                    lesson_name=(lesson.name),
                    status="locked",
                    opened_at=None,
                    closed_at=None,
                    created_at=now,
                    updated_at=now,
                )

                created = self.lesson_opening_repository.create(
                    entity=entity,
                    university_id=university_id,
                    class_section_lesson_plan_id=(
                        class_section_plan.class_section_lesson_plan_id
                    ),
                    lesson_id=lesson.lesson_id,
                )

                created_openings.append(created)

        return created_openings
