from apps.lessons.application.dto.create_subject_lesson_plan_dto import (
    CreateSubjectLessonPlanDTO,
)

from apps.lessons.domain.entities.subject_lesson_plan_entity import (
    SubjectLessonPlan,
)


class CreateSubjectLessonPlanUseCase:

    def __init__(
        self,
        repository,
        university_repository,
        lesson_repository,
        id_generator,
    ):
        self.repository = repository
        self.university_repository = university_repository
        self.lesson_repository = lesson_repository
        self.id_generator = id_generator

    def execute(
        self,
        dto: CreateSubjectLessonPlanDTO,
        university_id: str,
    ):

        # =========================================
        # UNIVERSITY
        # =========================================

        university = self.university_repository.find_by_id(university_id)

        if not university:
            raise ValueError("Không tìm thấy trường đại học.")

        # =========================================
        # COMMON LESSON RANGE
        # =========================================

        max_lesson_number = self.lesson_repository.get_max_lesson_number(
            university_id=university_id,
        )

        if max_lesson_number <= 0:
            raise ValueError("Trường chưa cấu hình buổi học chung.")

        # =========================================
        # SEMESTER
        # =========================================

        if dto.semester_number not in (
            "1",
            "2",
            "3",
        ):
            raise ValueError("Học kỳ không hợp lệ.")

        # =========================================
        # RULES
        # =========================================

        if not dto.rules:
            raise ValueError("Phải có ít nhất một quy tắc.")

        rules_by_type = {
            "theory": [],
            "practice": [],
        }

        for rule in dto.rules:

            # -----------------------------------------
            # LESSON TYPE
            # -----------------------------------------

            if rule.lesson_type not in (
                "theory",
                "practice",
            ):
                raise ValueError("Loại môn học không hợp lệ.")

            # -----------------------------------------
            # TOTAL LESSONS
            # -----------------------------------------

            if rule.total_lessons < 1:
                raise ValueError("Tổng số buổi phải lớn hơn 0.")

            if rule.total_lessons > max_lesson_number:
                raise ValueError(
                    f"Tổng số buổi ({rule.total_lessons}) "
                    f"không được vượt quá số buổi chung "
                    f"của trường ({max_lesson_number})."
                )

            # -----------------------------------------
            # MIN CREDITS
            # -----------------------------------------

            if rule.min_credits is not None:

                if rule.min_credits < 0:
                    raise ValueError("Tín chỉ tối thiểu không hợp lệ.")

            # -----------------------------------------
            # MAX CREDITS
            # -----------------------------------------

            if rule.max_credits is not None:

                if rule.max_credits < 0:
                    raise ValueError("Tín chỉ tối đa không hợp lệ.")

            # -----------------------------------------
            # MIN <= MAX
            # -----------------------------------------

            if (
                rule.min_credits is not None
                and rule.max_credits is not None
                and rule.min_credits > rule.max_credits
            ):
                raise ValueError(
                    "Tín chỉ tối thiểu không được " "lớn hơn tín chỉ tối đa."
                )

            rules_by_type[rule.lesson_type].append(rule)

        # =========================================
        # REQUIRE THEORY
        # =========================================

        if not rules_by_type["theory"]:

            raise ValueError("Phải có ít nhất một quy tắc lý thuyết.")

        # =========================================
        # REQUIRE PRACTICE
        # =========================================

        if not rules_by_type["practice"]:

            raise ValueError("Phải có ít nhất một quy tắc thực hành.")

        # =========================================
        # CHECK OVERLAP
        # =========================================

        for lesson_type, rules in rules_by_type.items():

            for i in range(len(rules)):

                first = rules[i]

                first_min = (
                    first.min_credits
                    if first.min_credits is not None
                    else float("-inf")
                )

                first_max = (
                    first.max_credits if first.max_credits is not None else float("inf")
                )

                for j in range(
                    i + 1,
                    len(rules),
                ):

                    second = rules[j]

                    second_min = (
                        second.min_credits
                        if second.min_credits is not None
                        else float("-inf")
                    )

                    second_max = (
                        second.max_credits
                        if second.max_credits is not None
                        else float("inf")
                    )

                    overlap = first_min <= second_max and second_min <= first_max

                    if overlap:

                        raise ValueError(
                            f"Các quy tắc {lesson_type} " "có khoảng tín chỉ bị trùng."
                        )

        # =========================================
        # CHECK EXISTING RULE
        # =========================================

        for rule in dto.rules:

            exists = self.repository.exists_rule(
                university_id=university_id,
                semester_number=(dto.semester_number),
                lesson_type=rule.lesson_type,
                min_credits=rule.min_credits,
                max_credits=rule.max_credits,
            )

            if exists:

                raise ValueError("Quy tắc này đã tồn tại.")

        # =========================================
        # CREATE
        # =========================================

        result = []

        for rule in dto.rules:

            subject_lesson_plan_id = self.id_generator.generate(
                university=university,
            )

            lesson_plan = SubjectLessonPlan(
                subject_lesson_plan_id=(subject_lesson_plan_id),
                university_id=university_id,
                semester_number=(dto.semester_number),
                lesson_type=rule.lesson_type,
                min_credits=rule.min_credits,
                max_credits=rule.max_credits,
                total_lessons=rule.total_lessons,
                is_custom=True,
            )

            created = self.repository.create(lesson_plan)

            result.append(created)

        return result
