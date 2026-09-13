from apps.lessons.application.dto.create_lesson_dto import (
    CreateLessonDTO,
)

from apps.lessons.domain.entities.lesson_entity import (
    Lesson,
)


class CreateLessonUseCase:

    def __init__(
        self,
        lesson_repository,
    ):
        self.lesson_repository = lesson_repository

    def execute(
        self,
        dto: CreateLessonDTO,
        university_id: str,
    ):

        # =====================================================
        # VALIDATE CREATE MODE
        # =====================================================

        if dto.create_mode not in (
            "single",
            "multiple",
        ):
            raise ValueError("Kiểu tạo buổi học không hợp lệ.")

        # =====================================================
        # SINGLE
        # =====================================================

        if dto.create_mode == "single":

            if dto.lesson_number is None or dto.lesson_number < 1:
                raise ValueError("Số buổi học không hợp lệ.")

            lesson_numbers = [dto.lesson_number]

        # =====================================================
        # MULTIPLE
        # =====================================================

        else:

            if dto.lesson_number_start is None or dto.lesson_number_end is None:
                raise ValueError("Vui lòng nhập buổi bắt đầu và buổi kết thúc.")

            if dto.lesson_number_start < 1:
                raise ValueError("Buổi bắt đầu phải lớn hơn 0.")

            if dto.lesson_number_end < dto.lesson_number_start:
                raise ValueError("Buổi kết thúc không được nhỏ hơn buổi bắt đầu.")

            lesson_numbers = list(
                range(
                    dto.lesson_number_start,
                    dto.lesson_number_end + 1,
                )
            )

        # =====================================================
        # VALIDATE ALL LESSON NUMBERS
        # =====================================================

        for lesson_number in lesson_numbers:

            exists = self.lesson_repository.exists_by_number(
                university_id=university_id,
                lesson_number=lesson_number,
            )

            if exists:

                raise ValueError(f"Buổi {lesson_number} đã tồn tại.")

        # =====================================================
        # CREATE LESSONS
        # =====================================================

        result = []

        for lesson_number in lesson_numbers:

            lesson = Lesson(
                lesson_id=f"L{lesson_number:03d}",
                lesson_number=lesson_number,
                name=f"Buổi {lesson_number}",
                university_id=university_id,
            )

            created = self.lesson_repository.create(
                lesson=lesson,
            )

            result.append(created)

        return result
