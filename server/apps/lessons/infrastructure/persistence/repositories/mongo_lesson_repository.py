from apps.lessons.domain.entities.lesson_entity import Lesson
from apps.lessons.domain.repositories.lesson_repository import (
    LessonRepository,
)

from apps.lessons.infrastructure.persistence.models.lesson_model import (
    LessonModel,
)

from apps.universities.infrastructure.persistence.models.university_model import (
    UniversityModel,
)


class MongoLessonRepository(LessonRepository):

    def get_by_university(
        self,
        university_id: str,
    ) -> list[Lesson]:

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return []

        lessons = LessonModel.objects(
            university=university,
        ).order_by("lesson_number")

        return [
            Lesson(
                lesson_id=lesson.lesson_id,
                lesson_number=lesson.lesson_number,
                name=lesson.name,
                university_id=university.university_id,
            )
            for lesson in lessons
        ]

    # =========================================
    # EXISTS BY LESSON NUMBER
    # =========================================

    def exists_by_number(
        self,
        university_id: str,
        lesson_number: int,
    ) -> bool:

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return False

        return (
            LessonModel.objects(
                university=university,
                lesson_number=lesson_number,
            ).first()
            is not None
        )

    # =========================================
    # CREATE
    # =========================================

    def create(
        self,
        lesson: Lesson,
    ) -> Lesson:

        university = UniversityModel.objects(
            university_id=lesson.university_id,
        ).first()

        if not university:
            raise ValueError("Không tìm thấy trường đại học.")

        lesson_model = LessonModel(
            lesson_id=lesson.lesson_id,
            lesson_number=lesson.lesson_number,
            name=lesson.name,
            university=university,
        )

        lesson_model.save()

        return lesson

    def get_max_lesson_number(
        self,
        university_id: str,
    ) -> int:

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return 0

        lesson = (
            LessonModel.objects(
                university=university,
            )
            .order_by("-lesson_number")
            .first()
        )

        if not lesson:
            return 0

        return lesson.lesson_number

    def count_by_university(
        self,
        university_id: str,
    ) -> int:

        university = UniversityModel.objects(
            university_id=university_id,
        ).first()

        if not university:
            return 0

        return LessonModel.objects(
            university=university,
        ).count()

    def get_by_university_and_lesson_range(
        self,
        university_id: str,
        total_lessons: int,
    ):

        university = (
            UniversityModel.objects(
                university_id=university_id,
            ).first()
        )

        if not university:
            return []


        return list(
            LessonModel.objects(
                university=university,
                lesson_number__lte=total_lessons,
            ).order_by(
                "lesson_number"
            )
        )