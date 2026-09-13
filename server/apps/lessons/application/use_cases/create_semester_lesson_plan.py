from apps.lessons.domain.entities.semester_lesson_plan_entity import (
    SemesterLessonPlan,
)


class CreateSemesterLessonPlanUseCase:

    def __init__(
        self,
        university_repository,
        academic_year_repository,
        semester_repository,
        semester_lesson_plan_repository,
        subject_lesson_plan_repository,
        semester_lesson_plan_id_generator,
        lesson_repository,
    ):

        self.university_repository = university_repository

        self.academic_year_repository = academic_year_repository

        self.semester_repository = semester_repository

        self.semester_lesson_plan_repository = semester_lesson_plan_repository

        self.subject_lesson_plan_repository = subject_lesson_plan_repository

        self.semester_lesson_plan_id_generator = semester_lesson_plan_id_generator

        self.lesson_repository = lesson_repository

    def execute(
        self,
        university_id: str,
        dto,
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
        # ACADEMIC YEAR
        # =====================================================

        academic_year = self.academic_year_repository.get_by_id(
            university_id=university_id,
            academic_year_id=dto.academic_year_id,
        )

        if not academic_year:
            raise ValueError("Không tìm thấy năm học.")

        # =====================================================
        # LESSON MASTER COUNT
        # =====================================================

        lesson_count = self.lesson_repository.count_by_university(
            university_id=university_id,
        )

        if lesson_count <= 0:
            raise ValueError("Trường chưa có buổi học mẫu.")

        # =====================================================
        # VALIDATE DUPLICATE SEMESTER NUMBER
        # =====================================================

        semester_numbers = set()

        for item in dto.semesters:

            if item.semester_number in semester_numbers:

                raise ValueError(f"Trùng học kỳ " f"{item.semester_number}.")

            semester_numbers.add(item.semester_number)

        # =====================================================
        # VALIDATE ALL FIRST
        # =====================================================

        validated_items = []

        for item in dto.semesters:

            semester = self.semester_repository.get_by_number(
                university_id=university_id,
                academic_year_id=(academic_year.academic_year_id),
                semester_number=item.semester_number,
            )

            if not semester:

                raise ValueError(
                    f"Không tìm thấy học kỳ "
                    f"{item.semester_number} "
                    f"trong năm học "
                    f"'{academic_year.name}'."
                )

            # -------------------------------------------------
            # TOTAL LESSON <= LESSON MASTER
            # -------------------------------------------------

            if item.total_lessons > lesson_count:

                raise ValueError(
                    f"Học kỳ {semester.name} yêu cầu "
                    f"{item.total_lessons} buổi, "
                    f"nhưng trường chỉ có "
                    f"{lesson_count} buổi học mẫu."
                )

            # -------------------------------------------------
            # EXISTING PLAN
            # -------------------------------------------------

            exists = self.semester_lesson_plan_repository.exists_by_semester(
                university_id=university_id,
                semester_id=semester.semester_id,
            )

            if exists:

                raise ValueError(
                    f"Kế hoạch học kỳ " f"'{semester.name}' " f"đã tồn tại."
                )

            # -------------------------------------------------
            # SUBJECT LESSON PLAN RULES
            # -------------------------------------------------

            rules = self.subject_lesson_plan_repository.get_rules_by_semester_number(
                university_id=university_id,
                semester_number=(semester.semester_number),
            )

            # -------------------------------------------------
            # SEMESTER TOTAL MUST COVER ALL RULES
            # -------------------------------------------------

            for rule in rules:

                if item.total_lessons < rule.total_lessons:

                    raise ValueError(
                        f"Học kỳ "
                        f"'{semester.name}' "
                        f"chỉ có "
                        f"{item.total_lessons} buổi, "
                        f"không đủ cho quy tắc "
                        f"'{rule.lesson_type}' "
                        f"yêu cầu "
                        f"{rule.total_lessons} buổi."
                    )

            validated_items.append(
                (
                    item,
                    semester,
                )
            )

        # =====================================================
        # CREATE
        # =====================================================

        created_plans = []

        for item, semester in validated_items:

            plan_id = self.semester_lesson_plan_id_generator.generate(
                semester_id=semester.semester_id,
            )

            entity = SemesterLessonPlan(
                semester_lesson_plan_id=plan_id,
                university_id=(university.university_id),
                semester_id=(semester.semester_id),
                academic_year_id=(academic_year.academic_year_id),
                academic_year_name=(academic_year.name),
                semester_number=(semester.semester_number),
                semester_name=(semester.name),
                total_lessons=(item.total_lessons),
            )

            created = self.semester_lesson_plan_repository.create(
                entity=entity,
                university_id=university_id,
                academic_year_id=(academic_year.academic_year_id),
            )

            created_plans.append(created)

        return created_plans
