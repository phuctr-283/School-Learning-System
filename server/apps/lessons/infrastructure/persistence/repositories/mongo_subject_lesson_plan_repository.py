from apps.lessons.domain.entities.subject_lesson_plan_entity import (
    SubjectLessonPlan,
)

from apps.lessons.domain.repositories.subject_lesson_plan_repository import (
    SubjectLessonPlanRepository,
)

from apps.lessons.infrastructure.persistence.models.subject_lesson_plan_model import (
    SubjectLessonPlanModel,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)


class MongoSubjectLessonPlanRepository(SubjectLessonPlanRepository):

    def create(
        self,
        subject_lesson_plan: SubjectLessonPlan,
    ) -> SubjectLessonPlan:

        university = UniversityModel.objects(
            university_id=(subject_lesson_plan.university_id),
        ).first()

        if not university:
            raise ValueError("Không tìm thấy trường đại học.")

        model = SubjectLessonPlanModel(
            subject_lesson_plan_id=(subject_lesson_plan.subject_lesson_plan_id),
            university=university,
            semester_number=(subject_lesson_plan.semester_number),
            lesson_type=(subject_lesson_plan.lesson_type),
            min_credits=(subject_lesson_plan.min_credits),
            max_credits=(subject_lesson_plan.max_credits),
            total_lessons=(subject_lesson_plan.total_lessons),
            is_custom=True,
        )

        model.save()

        return SubjectLessonPlan(
            subject_lesson_plan_id=(model.subject_lesson_plan_id),
            university_id=(university.university_id),
            semester_number=(model.semester_number),
            lesson_type=(model.lesson_type),
            min_credits=(model.min_credits),
            max_credits=(model.max_credits),
            total_lessons=(model.total_lessons),
            is_custom=model.is_custom,
        )

    def exists_rule(
        self,
        university_id: str,
        semester_number: str,
        lesson_type: str,
        min_credits,
        max_credits,
    ) -> bool:

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return False

        return (
            SubjectLessonPlanModel.objects(
                university=university,
                semester_number=semester_number,
                lesson_type=lesson_type,
                min_credits=min_credits,
                max_credits=max_credits,
            ).first()
            is not None
        )

    def get_subject_lesson_plans(
        self,
        university_id: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return []

        return list(
            SubjectLessonPlanModel.objects(
                university=university,
            ).order_by(
                "semester_number",
                "lesson_type",
                "min_credits",
            )
        )

    def get_by_semester_number(
        self,
        university_id: str,
        semester_number: str,
    ):

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return []

        return list(
            SubjectLessonPlanModel.objects(
                university=university,
                semester_number=semester_number,
            ).order_by(
                "lesson_type",
                "min_credits",
            )
        )

    def get_rule_for_subject(
    self,
    university_id: str,
    subject,
    semester_number: str,
):
        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return None

        if subject.subject_types == "Theory":
            lesson_type = "theory"

        elif subject.subject_types == "Practice":
            lesson_type = "practice"

        else:
            return None

        rules = SubjectLessonPlanModel.objects(
            university=university,
            semester_number=semester_number,
            lesson_type=lesson_type,
        )

        for rule in rules:

            if lesson_type == "practice":
                return rule

            if lesson_type == "theory":

                if (
                    rule.min_credits is not None
                    and subject.credits < rule.min_credits
                ):
                    continue

                if (
                    rule.max_credits is not None
                    and subject.credits > rule.max_credits
                ):
                    continue

                return rule

        return None

    def get_rules_by_semester_number(
        self,
        university_id: str,
        semester_number: str,
    ):
        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return []

        return list(
            SubjectLessonPlanModel.objects(
                university=university,
                semester_number=semester_number,
            ).order_by(
                "lesson_type",
                "min_credits",
            )
        )
