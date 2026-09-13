from apps.lessons.application.dto.lesson_dto import LessonDTO
from apps.lessons.domain.repositories.lesson_repository import (
    LessonRepository,
)


class GetLessonsUseCase:

    def __init__(
        self,
        lesson_repository: LessonRepository,
    ):
        self.lesson_repository = lesson_repository

    def execute(
        self,
        university_id: str,
    ) -> list[LessonDTO]:

        lessons = self.lesson_repository.get_by_university(
            university_id=university_id,
        )

        return [
            LessonDTO(
                lesson_id=lesson.lesson_id,
                lesson_number=lesson.lesson_number,
                name=lesson.name,
                university_id=lesson.university_id,
            )
            for lesson in lessons
        ]