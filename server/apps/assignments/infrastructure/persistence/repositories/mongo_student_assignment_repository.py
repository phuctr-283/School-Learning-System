import json
import random
from datetime import (
    datetime,
    timezone,
    timedelta,
)
from decimal import Decimal

from apps.assignments.domain.repositories.student_assignment_repository import (
    StudentAssignmentRepository,
)

from apps.assignments.infrastructure.persistence.models.assignment_attempt_model import (
    AssignmentAttemptModel,
)

from apps.assignments.infrastructure.persistence.models.assignment_application_model import (
    AssignmentApplicationModel,
)

from apps.class_sections.infrastructure.persistence.models.class_section_model import (
    ClassSectionModel,
)

from apps.class_sections.infrastructure.persistence.models.class_section_student_model import (
    ClassSectionStudentModel,
)

from apps.lessons.infrastructure.persistence.models.class_section_lesson_plan_model import (
    ClassSectionLessonPlanModel,
)

from apps.students.infrastructure.persistence.models.student_model import (
    StudentModel,
)

from apps.assignments.infrastructure.services.attempt_id_generator import (
    generate_attempt_id,
)

from apps.assignments.application.dto.student_assignment_dto import (
    StudentAssignmentContentDTO,
    StudentAssignmentOptionDTO,
    StudentAssignmentQuestionDTO,
    StudentAssignmentResultDTO,
    StudentAssignmentReviewDTO,
)
from apps.assignments.application.exceptions.assignment_exceptions import (
    AssignmentBadRequestError,
    AssignmentForbiddenError,
    AssignmentLockedError,
    AssignmentNotFoundError,
)
from apps.assignments.application.dto.assignment_attempt_history_dto import (
    AssignmentHistoryDTO,
    AssignmentHistoryOptionDTO,
    AssignmentHistoryQuestionDTO,
)


class MongoStudentAssignmentRepository(
    StudentAssignmentRepository,
):

    def _now(self):
        return datetime.now(timezone.utc)

    def _to_utc(self, value):

        if value is None:
            return None

        if value.tzinfo is None:
            return value.replace(
                tzinfo=timezone.utc,
            )

        return value.astimezone(
            timezone.utc,
        )

    def _normalize_answer(self, value):

        if value is None:
            return None

        if isinstance(value, str):

            value = value.strip()

            if not value:
                return None

            try:
                return json.loads(value)
            except (
                json.JSONDecodeError,
                TypeError,
            ):
                return value

        return value

    def _get_student(
        self,
        student_id,
    ):
        normalized_student_id = str(student_id).strip().upper()

        student = (
            StudentModel.objects(
                student_id=normalized_student_id,
            )
            .first()
            .select_related()
        )

        if student is None:
            raise AssignmentNotFoundError("Không tìm thấy sinh viên.")

        if not getattr(
            student,
            "is_active",
            True,
        ):
            raise AssignmentForbiddenError("Tài khoản sinh viên đã bị khóa.")

        return student

    def _get_class_section(
        self,
        class_section_id,
    ):

        class_section = (
            ClassSectionModel.objects(
                class_section_id=str(
                    class_section_id,
                ).strip(),
                status="active",
            )
            .first()
            .select_related()
        )

        if class_section is None:
            raise AssignmentNotFoundError("Không tìm thấy lớp học phần đang hoạt động.")

        return class_section

    def _validate_enrollment(
        self,
        student,
        class_section,
    ):

        enrollment = ClassSectionStudentModel.objects(
            student=student,
            class_section=class_section,
        ).first()

        if enrollment is None:
            raise AssignmentForbiddenError("Sinh viên không thuộc lớp học phần này.")

        return enrollment

    def _get_application(
        self,
        assignment_application_id,
        lesson_id,
    ):

        application = (
            AssignmentApplicationModel.objects(
                assignment_application_id=str(
                    assignment_application_id,
                ).strip(),
            )
            .first()
            .select_related()
        )

        if application is None:
            raise AssignmentNotFoundError("Không tìm thấy bài tập.")

        if str(application.lesson_id) != str(lesson_id):
            raise AssignmentBadRequestError("Bài tập không thuộc bài học này.")

        if application.status != "published":
            raise AssignmentLockedError("Bài tập hiện không khả dụng.")

        return application

    def _get_class_section_state(
        self,
        application,
        class_section_id,
    ):

        target_id = str(
            class_section_id,
        ).strip()

        for item in application.class_sections or []:

            if not item.class_section:
                continue

            current_id = str(item.class_section.class_section_id)

            if current_id != target_id:
                continue

            if item.status != "active":
                raise AssignmentLockedError(
                    "Bài tập hiện đã được tắt cho lớp học phần này."
                )

            return item

        raise AssignmentLockedError("Bài tập không áp dụng cho lớp học phần này.")

    def _validate_lesson_opening(
        self,
        class_section,
        lesson_id,
    ):

        lesson_plan = (
            ClassSectionLessonPlanModel.objects(
                class_section=class_section,
            )
            .first()
            .select_related()
        )

        if lesson_plan is None:
            raise AssignmentNotFoundError("Không tìm thấy kế hoạch bài học.")

        for opening in lesson_plan.lesson_openings or []:

            if not opening.lesson:
                continue

            if str(opening.lesson.lesson_id) != str(lesson_id):
                continue

            if opening.status != "open":
                raise AssignmentLockedError("Buổi học hiện chưa được mở.")

            return opening

        raise AssignmentNotFoundError("Không tìm thấy buổi học trong kế hoạch lớp.")

    def _get_attempt_deadline(
        self,
        attempt,
        application,
        assignment,
    ):

        started_at = self._to_utc(
            attempt.started_at,
        )

        duration_deadline = started_at + timedelta(
            minutes=int(assignment.duration_minutes)
        )

        due_at = self._to_utc(
            application.due_at,
        )

        if due_at is None:
            return duration_deadline

        return min(
            duration_deadline,
            due_at,
        )

    def _get_or_create_attempt(
        self,
        application,
        student,
        class_section,
    ):

        now = self._now()

        attempt = (
            AssignmentAttemptModel.objects(
                assignment_application=application,
                student=student,
                class_section=class_section,
                status="in_progress",
            )
            .order_by("-started_at")
            .first()
        )

        if attempt is not None:

            assignment = application.assignment

            if assignment is None:
                raise AssignmentNotFoundError("Không tìm thấy nội dung bài tập.")

            deadline = self._get_attempt_deadline(
                attempt,
                application,
                assignment,
            )

            # Hết giờ → tự động chấm
            if now >= deadline:

                self._grade_attempt(
                    attempt,
                    assignment,
                )

                return attempt

            return attempt

        graded_attempt = (
            AssignmentAttemptModel.objects(
                assignment_application=application,
                student=student,
                class_section=class_section,
                status="graded",
            )
            .order_by("-submitted_at")
            .first()
        )

        if graded_attempt is not None:

            raise AssignmentLockedError("Bài tập này đã được nộp và không thể làm lại.")

        used_attempts = AssignmentAttemptModel.objects(
            assignment_application=application,
            student=student,
            class_section=class_section,
        ).count()

        max_attempts = int(application.max_attempts or 1)

        if used_attempts >= max_attempts:

            raise AssignmentLockedError("Bạn đã sử dụng hết số lần làm bài.")

        assignment = application.assignment

        if assignment is None:
            raise ValueError("Không tìm thấy nội dung bài tập.")

        attempt = AssignmentAttemptModel(
            attempt_id=generate_attempt_id(),
            assignment_application=application,
            student=student,
            class_section=class_section,
            status="in_progress",
            started_at=now,
            answers={},
            total_score=assignment.total_score,
            answered_count=0,
        )

        attempt.save()

        return attempt

    def _sanitize_answers(
        self,
        assignment,
        answers,
    ):

        if not isinstance(
            answers,
            dict,
        ):
            return {}

        valid_questions = {
            str(question.question_id): question
            for question in (assignment.questions or [])
        }

        result = {}

        for question_id, value in answers.items():

            question = valid_questions.get(str(question_id))

            if question is None:
                continue

            question_type = question.question_type

            valid_option_ids = {
                str(option.option_id) for option in (question.options or [])
            }

            if question_type == "multiple_choice":

                value = self._normalize_answer(value)

                if value is not None and str(value) in valid_option_ids:
                    result[str(question_id)] = str(value)

            elif question_type in (
                "ordering",
                "drag_and_drop",
            ):

                value = self._normalize_answer(value)

                if not isinstance(
                    value,
                    list,
                ):
                    continue

                clean_values = []

                used_options = set()

                for option_id in value:

                    if option_id is None:

                        if question_type == "drag_and_drop":
                            clean_values.append(None)

                        continue

                    option_id = str(option_id)

                    if option_id not in valid_option_ids:
                        continue

                    if option_id in used_options:
                        continue

                    used_options.add(option_id)

                    clean_values.append(option_id)

                if question_type == "drag_and_drop":

                    blank_count = int(question.blank_count or 0)

                    clean_values = clean_values[:blank_count]

                result[str(question_id)] = clean_values

        return result

    def _answers_equal(
        self,
        question,
        user_answer,
    ):

        if question.answer is None:
            return False

        user_answer = self._normalize_answer(user_answer)

        if user_answer is None:
            return False

        if question.question_type == "multiple_choice":

            correct_ids = [
                str(option_id)
                for option_id in (question.answer.correct_option_ids or [])
            ]

            return str(user_answer) in correct_ids

        if question.question_type in (
            "ordering",
            "drag_and_drop",
        ):

            correct_order = [
                (None if option_id is None else str(option_id))
                for option_id in (question.answer.correct_order_option_ids or [])
            ]

            if not isinstance(
                user_answer,
                list,
            ):
                return False

            normalized_user = [
                (None if value is None else str(value)) for value in user_answer
            ]

            return normalized_user == correct_order

        return False

    def _build_questions(
        self,
        assignment,
    ):

        questions = []

        for question in sorted(
            assignment.questions or [],
            key=lambda item: item.order,
        ):

            source_options = list(question.options or [])

            if question.shuffle_options:
                random.shuffle(source_options)
            else:
                source_options.sort(key=lambda item: item.order)

            options = [
                StudentAssignmentOptionDTO(
                    option_id=str(option.option_id),
                    content=option.content,
                    order=option.order,
                )
                for option in source_options
            ]

            questions.append(
                StudentAssignmentQuestionDTO(
                    question_id=str(question.question_id),
                    question=question.question,
                    content=question.content,
                    question_type=question.question_type,
                    score=question.score,
                    order=question.order,
                    shuffle_options=bool(question.shuffle_options),
                    blank_count=int(question.blank_count or 0),
                    options=options,
                )
            )

        return questions

    def _build_correct_answer(
        self,
        question,
    ):

        if question.answer is None:
            return None

        if question.question_type == "multiple_choice":

            return {
                "correct_option_ids": [
                    str(option_id)
                    for option_id in (question.answer.correct_option_ids or [])
                ]
            }

        if question.question_type in (
            "ordering",
            "drag_and_drop",
        ):

            return {
                "correct_order_option_ids": [
                    (None if option_id is None else str(option_id))
                    for option_id in (question.answer.correct_order_option_ids or [])
                ]
            }

        return {
            "correct_answers": [
                str(answer) for answer in (question.answer.correct_answers or [])
            ]
        }

    def _grade_attempt(
        self,
        attempt,
        assignment,
    ):

        answers = attempt.answers or {}

        score = Decimal("0.00")

        correct_count = 0
        answered_count = 0

        review = []

        for question in assignment.questions or []:

            question_id = str(question.question_id)

            user_answer = answers.get(question_id)

            if user_answer not in (
                None,
                "",
                [],
            ):
                answered_count += 1

            is_correct = self._answers_equal(
                question,
                user_answer,
            )

            question_score = Decimal(str(question.score))

            earned_score = question_score if is_correct else Decimal("0.00")

            if is_correct:
                score += question_score
                correct_count += 1

            review.append(
                StudentAssignmentReviewDTO(
                    question_id=question_id,
                    question_type=(question.question_type),
                    user_answer=user_answer,
                    correct=is_correct,
                    score=earned_score,
                    correct_answer=(self._build_correct_answer(question)),
                )
            )

        total_score = Decimal(str(assignment.total_score))

        percentage = Decimal("0.00")

        if total_score > 0:

            percentage = score / total_score * Decimal("100")

        now = self._now()

        attempt.status = "graded"
        attempt.submitted_at = now
        attempt.score = score
        attempt.total_score = total_score
        attempt.answered_count = answered_count
        attempt.updated_at = now

        attempt.save()

        return StudentAssignmentResultDTO(
            score=score,
            total_score=total_score,
            percentage=percentage,
            answered_count=answered_count,
            correct_count=correct_count,
            submitted_at=now,
            review=review,
        )

    def _get_attempt_result(
        self,
        attempt,
        assignment,
    ):

        answers = attempt.answers or {}

        correct_count = 0

        review = []

        for question in assignment.questions or []:

            question_id = str(question.question_id)

            user_answer = answers.get(question_id)

            is_correct = self._answers_equal(
                question,
                user_answer,
            )

            if is_correct:
                correct_count += 1

            review.append(
                StudentAssignmentReviewDTO(
                    question_id=question_id,
                    question_type=(question.question_type),
                    user_answer=user_answer,
                    correct=is_correct,
                    score=(question.score if is_correct else Decimal("0.00")),
                    correct_answer=(self._build_correct_answer(question)),
                )
            )

        total_score = Decimal(str(attempt.total_score or 0))

        score = Decimal(str(attempt.score or 0))

        percentage = Decimal("0.00")

        if total_score > 0:
            percentage = score / total_score * Decimal("100")

        return StudentAssignmentResultDTO(
            score=score,
            total_score=total_score,
            percentage=percentage,
            answered_count=(attempt.answered_count or 0),
            correct_count=correct_count,
            submitted_at=attempt.submitted_at,
            review=review,
        )

    def _build_assignment_response(
        self,
        application,
        attempt,
        assignment,
    ):

        now = self._now()

        deadline = self._get_attempt_deadline(
            attempt,
            application,
            assignment,
        )

        remaining_seconds = max(
            0,
            int((deadline - now).total_seconds()),
        )

        result = None

        if attempt.status == "graded":

            result = self._get_attempt_result(
                attempt,
                assignment,
            )

        return StudentAssignmentContentDTO(
            assignment_application_id=str(application.assignment_application_id),
            assignment_id=str(assignment.assignment_id),
            lesson_id=str(application.lesson_id),
            title=assignment.title,
            description=assignment.description,
            subject_id=str(assignment.subject.subject_id),
            subject_name=assignment.subject.name,
            assignment_type=assignment.assignment_type,
            total_score=assignment.total_score,
            duration_minutes=int(assignment.duration_minutes),
            max_attempts=int(application.max_attempts or 1),
            open_at=application.open_at,
            due_at=application.due_at,
            attempt_id=str(attempt.attempt_id),
            attempt_status=attempt.status,
            started_at=attempt.started_at,
            deadline_at=deadline,
            remaining_seconds=remaining_seconds,
            saved_answers=attempt.answers or {},
            questions=self._build_questions(assignment),
            result=result,
        )

    def get_student_assignment(
        self,
        student_id,
        assignment_application_id,
        class_section_id,
        lesson_id,
    ):

        student = self._get_student(student_id)

        class_section = self._get_class_section(class_section_id)

        self._validate_enrollment(
            student,
            class_section,
        )

        application = self._get_application(
            assignment_application_id,
            lesson_id,
        )

        self._get_class_section_state(
            application,
            class_section_id,
        )

        self._validate_lesson_opening(
            class_section,
            lesson_id,
        )

        assignment = application.assignment

        if assignment is None:
            raise AssignmentNotFoundError("Không tìm thấy nội dung bài tập.")

        now = self._now()

        open_at = self._to_utc(application.open_at)

        due_at = self._to_utc(application.due_at)
        if open_at and now < open_at:
            raise AssignmentLockedError("Bài tập chưa đến thời gian mở.")

        if due_at and now > due_at:
            raise AssignmentLockedError("Bài tập đã hết hạn.")
        attempt = self._get_or_create_attempt(
            application,
            student,
            class_section,
        )

        return self._build_assignment_response(
            application,
            attempt,
            assignment,
        )

    def save_answers(
        self,
        student_id,
        assignment_application_id,
        class_section_id,
        lesson_id,
        attempt_id,
        answers,
    ):

        student = self._get_student(student_id)

        class_section = self._get_class_section(class_section_id)

        self._validate_enrollment(
            student,
            class_section,
        )

        application = self._get_application(
            assignment_application_id,
            lesson_id,
        )

        self._get_class_section_state(
            application,
            class_section_id,
        )

        self._validate_lesson_opening(
            class_section,
            lesson_id,
        )

        assignment = application.assignment

        if assignment is None:
            raise AssignmentNotFoundError("Không tìm thấy nội dung bài tập.")

        attempt = AssignmentAttemptModel.objects(
            attempt_id=attempt_id,
            assignment_application=application,
            student=student,
            class_section=class_section,
        ).first()

        if attempt is None:
            raise AssignmentNotFoundError("Không tìm thấy lượt làm bài.")

        if attempt.status != "in_progress":

            return {
                "saved": False,
                "status": attempt.status,
                "remaining_seconds": 0,
            }

        now = self._now()

        deadline = self._get_attempt_deadline(
            attempt,
            application,
            assignment,
        )

        clean_answers = self._sanitize_answers(
            assignment,
            answers,
        )

        attempt.answers = clean_answers

        attempt.answered_count = sum(
            1
            for value in clean_answers.values()
            if value
            not in (
                None,
                "",
                [],
            )
        )

        attempt.updated_at = now

        if now >= deadline:

            result = self._grade_attempt(
                attempt,
                assignment,
            )

            return {
                "saved": True,
                "expired": True,
                "status": "graded",
                "remaining_seconds": 0,
                "deadline_at": deadline,
                "result": result,
            }

        attempt.save()

        return {
            "saved": True,
            "expired": False,
            "status": "in_progress",
            "remaining_seconds": max(
                0,
                int((deadline - now).total_seconds()),
            ),
            "deadline_at": deadline,
        }

    def submit_assignment(
        self,
        student_id,
        assignment_application_id,
        class_section_id,
        lesson_id,
        attempt_id,
        answers,
    ):

        student = self._get_student(student_id)

        class_section = self._get_class_section(class_section_id)

        self._validate_enrollment(
            student,
            class_section,
        )

        application = self._get_application(
            assignment_application_id,
            lesson_id,
        )

        self._get_class_section_state(
            application,
            class_section_id,
        )

        assignment = application.assignment

        if assignment is None:
            raise AssignmentNotFoundError("Không tìm thấy nội dung bài tập.")

        attempt = AssignmentAttemptModel.objects(
            attempt_id=attempt_id,
            assignment_application=application,
            student=student,
            class_section=class_section,
        ).first()

        if attempt is None:
            raise AssignmentNotFoundError("Không tìm thấy lượt làm bài.")

        if attempt.status == "graded":

            return self._get_attempt_result(
                attempt,
                assignment,
            )

        attempt.answers = self._sanitize_answers(
            assignment,
            answers,
        )

        attempt.answered_count = sum(
            1
            for value in attempt.answers.values()
            if value
            not in (
                None,
                "",
                [],
            )
        )

        attempt.updated_at = self._now()

        attempt.save()

        return self._grade_attempt(
            attempt,
            assignment,
        )

    def _get_graded_attempt(
        self,
        application,
        student,
        class_section,
    ):
        attempt = (
            AssignmentAttemptModel.objects(
                assignment_application=application,
                student=student,
                class_section=class_section,
                status="graded",
            )
            .order_by("-submitted_at")
            .first()
        )

        if attempt is None:
            raise AssignmentNotFoundError("Không tìm thấy bài làm đã chấm.")

        return attempt

    def _get_correct_answer_for_history(
        self,
        question,
    ):
        if question.answer is None:
            return None

        if question.question_type == "multiple_choice":

            return [
                str(option_id)
                for option_id in (question.answer.correct_option_ids or [])
            ]

        if question.question_type in (
            "ordering",
            "drag_and_drop",
        ):

            return [
                (None if option_id is None else str(option_id))
                for option_id in (question.answer.correct_order_option_ids or [])
            ]

        return [str(answer) for answer in (question.answer.correct_answers or [])]

    def _normalize_history_answer(
        self,
        value,
    ):
        if value is None:
            return None

        if isinstance(value, str):

            try:
                return json.loads(value)

            except (
                json.JSONDecodeError,
                TypeError,
            ):
                return value

        if isinstance(value, list):

            return [(None if item is None else str(item)) for item in value]

        return value

    def _build_history_options(
        self,
        question,
        user_answer,
    ):
        correct_option_ids = set()

        if question.answer is not None:

            correct_option_ids = {
                str(option_id)
                for option_id in (question.answer.correct_option_ids or [])
            }

        selected_option_ids = self._get_selected_option_ids(
            question,
            user_answer,
        )

        options = []

        for option in sorted(
            question.options or [],
            key=lambda item: item.order,
        ):

            option_id = str(option.option_id)
            is_correct = option_id in correct_option_ids

            is_selected = option_id in selected_option_ids

            is_selected_correct = is_selected and is_correct

            is_selected_wrong = is_selected and not is_correct

            options.append(
                AssignmentHistoryOptionDTO(
                    option_id=option_id,
                    content=option.content,
                    is_correct=is_correct,
                    is_selected=is_selected,
                    is_selected_correct=(is_selected_correct),
                    is_selected_wrong=(is_selected_wrong),
                )
            )

        return options

    def _build_history_question(
        self,
        question,
        user_answer,
    ):
        normalized_user_answer = self._normalize_history_answer(user_answer)

        correct_answer = self._get_correct_answer_for_history(question)

        correct = self._answers_equal(
            question,
            normalized_user_answer,
        )

        question_score = Decimal(str(question.score))

        earned_score = question_score if correct else Decimal("0.00")

        options = self._build_history_options(
            question=question,
            user_answer=normalized_user_answer,
        )

        correct_options = [option for option in options if option.is_correct]

        wrong_options = [option for option in options if not option.is_correct]

        return AssignmentHistoryQuestionDTO(
            question_id=str(question.question_id),
            question=question.question,
            content=question.content,
            question_type=question.question_type,
            score=question_score,
            earned_score=earned_score,
            user_answer=normalized_user_answer,
            correct_answer=correct_answer,
            correct=correct,
            options=options,
            correct_options=correct_options,
            wrong_options=wrong_options,
        )

    def _build_assignment_history(
        self,
        application,
        attempt,
        assignment,
    ):
        answers = attempt.answers or {}

        questions = []

        correct_count = 0

        for question in sorted(
            assignment.questions or [],
            key=lambda item: item.order,
        ):

            question_id = str(question.question_id)

            user_answer = answers.get(question_id)

            history_question = self._build_history_question(
                question=question,
                user_answer=user_answer,
            )

            if history_question.correct:
                correct_count += 1

            questions.append(history_question)

        total_score = Decimal(str(attempt.total_score or assignment.total_score or 0))

        score = Decimal(str(attempt.score or 0))

        percentage = Decimal("0.00")

        if total_score > 0:

            percentage = score / total_score * Decimal("100")

        return AssignmentHistoryDTO(
            attempt_id=str(attempt.attempt_id),
            assignment_application_id=str(application.assignment_application_id),
            assignment_id=str(assignment.assignment_id),
            lesson_id=str(application.lesson_id),
            title=assignment.title,
            subject_name=assignment.subject.name,
            assignment_type=assignment.assignment_type,
            total_score=total_score,
            score=score,
            percentage=percentage,
            answered_count=int(attempt.answered_count or 0),
            correct_count=correct_count,
            started_at=attempt.started_at,
            submitted_at=attempt.submitted_at,
            questions=questions,
        )

    def _get_selected_option_ids(
        self,
        question,
        user_answer,
    ):
        if not user_answer:
            return set()

        if question.question_type == "multiple_choice":
            if isinstance(user_answer, list):
                return {str(option_id) for option_id in user_answer}

            return {str(user_answer)}

        if question.question_type in (
            "ordering",
            "drag_and_drop",
        ):
            if isinstance(user_answer, list):
                return {
                    str(option_id) for option_id in user_answer if option_id is not None
                }

        return set()

    def get_attempt_history(
        self,
        assignment_application_id,
        student_id,
        class_section_id,
    ):
        student = self._get_student(student_id)

        class_section = self._get_class_section(class_section_id)

        self._validate_enrollment(
            student,
            class_section,
        )

        application = (
            AssignmentApplicationModel.objects(
                assignment_application_id=str(assignment_application_id).strip(),
            )
            .first()
            .select_related()
        )

        if application is None:
            raise AssignmentNotFoundError("Không tìm thấy bài tập.")

        self._get_class_section_state(
            application,
            class_section_id,
        )

        assignment = application.assignment

        if assignment is None:
            raise AssignmentNotFoundError("Không tìm thấy nội dung bài tập.")

        attempt = self._get_graded_attempt(
            application=application,
            student=student,
            class_section=class_section,
        )

        return self._build_assignment_history(
            application=application,
            attempt=attempt,
            assignment=assignment,
        )
