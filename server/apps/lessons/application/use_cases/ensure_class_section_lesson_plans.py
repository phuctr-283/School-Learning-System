from apps.lessons.domain.entities.class_section_lesson_plan_entity import (
    ClassSectionLessonPlan,
)


class EnsureClassSectionLessonPlansUseCase:

    def __init__(
        self,
        class_section_repository,
        class_section_lesson_plan_repository,
        course_lesson_plan_repository,
        university_repository,
        class_section_lesson_plan_id_generator,
    ):

        self.class_section_repository = class_section_repository

        self.class_section_lesson_plan_repository = class_section_lesson_plan_repository

        self.course_lesson_plan_repository = course_lesson_plan_repository

        self.university_repository = university_repository

        self.class_section_lesson_plan_id_generator = (
            class_section_lesson_plan_id_generator
        )

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
        # GET ALL CLASS SECTIONS
        # =====================================================

        class_sections = self.class_section_repository.get_by_university(
            university_id=university_id,
        )

        created_plans = []

        # =====================================================
        # ENSURE CLASS SECTION LESSON PLAN
        # =====================================================

        for class_section in class_sections:

            # =================================================
            # CHECK EXISTING
            # =================================================

            exists = self.class_section_lesson_plan_repository.exists_by_class_section(
                university_id=university_id,
                class_section_id=(class_section.class_section_id),
            )

            if exists:
                continue

            # =================================================
            # GET COURSE LESSON PLAN
            # =================================================

            course_plan = (
                self.course_lesson_plan_repository.get_by_subject_and_semester(
                    university_id=university_id,
                    subject_id=(class_section.subject_id),
                    semester_id=(class_section.semester_id),
                )
            )

            if not course_plan:

                raise ValueError(
                    f"Chưa có kế hoạch môn học phần "
                    f"cho môn "
                    f"'{class_section.subject_name}', "
                    f"{class_section.semester_name}."
                )

            # =================================================
            # GENERATE ID
            #
            # CSLP-subject_id-group_number
            # =================================================

            plan_id = self.class_section_lesson_plan_id_generator.generate(
                subject_id=(class_section.subject_id),
                group_number=(class_section.group_number),
            )

            # =================================================
            # ENTITY
            # =================================================

            entity = ClassSectionLessonPlan(
                class_section_lesson_plan_id=(plan_id),
                university_id=(university.university_id),
                university_name=(university.name),
                course_lesson_plan_id=(course_plan.course_lesson_plan_id),
                class_section_id=(class_section.class_section_id),
                group_number=(class_section.group_number),
                subject_id=(class_section.subject_id),
                subject_name=(class_section.subject_name),
                semester_id=(class_section.semester_id),
                semester_name=(class_section.semester_name),
                semester_number=(class_section.semester_number),
                academic_year_id=(class_section.academic_year_id),
                academic_year_name=(class_section.academic_year_name),
                total_lessons=(course_plan.total_lessons),
                is_custom=False,
                custom_total_lessons=None,
                effective_total_lessons=(course_plan.total_lessons),
            )

            # =================================================
            # CREATE
            # =================================================

            created = self.class_section_lesson_plan_repository.create(
                entity=entity,
                university_id=university_id,
                class_section_id=(class_section.class_section_id),
                course_lesson_plan_id=(course_plan.course_lesson_plan_id),
            )

            created_plans.append(created)

        return created_plans
