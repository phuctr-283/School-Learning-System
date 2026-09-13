from apps.lessons.domain.entities.course_lesson_plan_entity import (
    CourseLessonPlan,
)


class EnsureCourseLessonPlansUseCase:

    def __init__(
        self,
        class_section_repository,
        course_lesson_plan_repository,
        subject_lesson_plan_repository,
        university_repository,
        subject_repository,
        semester_repository,
        course_lesson_plan_id_generator,
    ):

        self.class_section_repository = class_section_repository

        self.course_lesson_plan_repository = course_lesson_plan_repository

        self.subject_lesson_plan_repository = subject_lesson_plan_repository

        self.university_repository = university_repository

        self.subject_repository = subject_repository

        self.semester_repository = semester_repository

        self.course_lesson_plan_id_generator = course_lesson_plan_id_generator

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

        processed = set()

        # =====================================================
        # ENSURE COURSE LESSON PLAN
        #
        # Một Subject + Semester
        # chỉ có một CourseLessonPlan
        # =====================================================

        for class_section in class_sections:

            key = (
                class_section.subject_id,
                class_section.semester_id,
            )

            if key in processed:
                continue

            processed.add(key)

            # =================================================
            # CHECK EXISTING
            # =================================================

            existing = self.course_lesson_plan_repository.get_by_subject_and_semester(
                university_id=university_id,
                subject_id=class_section.subject_id,
                semester_id=class_section.semester_id,
            )

            if existing:
                continue

            # =================================================
            # GET SUBJECT
            # =================================================

            subject = self.subject_repository.get_by_id(
                university_id=university_id,
                subject_id=class_section.subject_id,
            )

            if not subject:
                raise ValueError(
                    f"Không tìm thấy môn " f"'{class_section.subject_name}'."
                )

            # =================================================
            # GET SUBJECT LESSON PLAN RULE
            #
            # Rule dựa trên:
            # - semester_number
            # - lesson_type
            # - credits
            # =================================================

            subject_plan = self.subject_lesson_plan_repository.get_rule_for_subject(
                university_id=university_id,
                subject=subject,
                semester_number=(class_section.semester_number),
            )

            if not subject_plan:

                raise ValueError(
                    f"Không tìm thấy quy tắc số buổi "
                    f"cho môn "
                    f"'{class_section.subject_name}' "
                    f"trong học kỳ "
                    f"{class_section.semester_number}."
                )

            # =================================================
            # GET SEMESTER
            # =================================================

            semester = self.semester_repository.get_by_id(
                university_id=university_id,
                semester_id=class_section.semester_id,
            )

            if not semester:

                raise ValueError(
                    f"Không tìm thấy học kỳ " f"'{class_section.semester_name}'."
                )

            # =================================================
            # GENERATE ID
            #
            # CLP-subject_id-semester_id
            # =================================================

            course_lesson_plan_id = self.course_lesson_plan_id_generator.generate(
                subject_id=class_section.subject_id,
                semester_id=class_section.semester_id,
            )

            # =================================================
            # ENTITY
            # =================================================

            entity = CourseLessonPlan(
                course_lesson_plan_id=(course_lesson_plan_id),
                university_id=(university.university_id),
                university_name=(university.name),
                subject_id=(subject.subject_id),
                subject_name=(subject.name),
                semester_id=(semester.semester_id),
                semester_name=(semester.name),
                semester_number=(semester.semester_number),
                academic_year_id=(semester.academic_year_id),
                academic_year_name=(semester.academic_year_name),
                total_lessons=(subject_plan.total_lessons),
            )

            # =================================================
            # CREATE
            # =================================================

            created = self.course_lesson_plan_repository.create(
                course_lesson_plan=entity,
                university=university,
                subject=subject,
                semester=semester,
            )

            created_plans.append(created)

        return created_plans
