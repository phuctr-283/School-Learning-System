from apps.assessment.domain.entities.assessment_question_answer_entity import (
    AssessmentQuestionAnswer,
)

from apps.assessment.infrastructure.persistence.models.assessment_question_answer_model import (
    AssessmentQuestionAnswerModel,
)


class AssessmentQuestionAnswerMapper:

    @staticmethod
    def to_model(
        entity: AssessmentQuestionAnswer,
    ) -> AssessmentQuestionAnswerModel:

        return AssessmentQuestionAnswerModel(
            correct_option_ids=list(
                entity.correct_option_ids,
            ),
            correct_order_option_ids=list(
                entity.correct_order_option_ids,
            ),
            correct_answers=list(
                entity.correct_answers,
            ),
        )

    @staticmethod
    def to_entity(
        model: AssessmentQuestionAnswerModel,
    ) -> AssessmentQuestionAnswer:

        return AssessmentQuestionAnswer(
            correct_option_ids=list(
                model.correct_option_ids or [],
            ),
            correct_order_option_ids=list(
                model.correct_order_option_ids or [],
            ),
            correct_answers=list(
                model.correct_answers or [],
            ),
        )