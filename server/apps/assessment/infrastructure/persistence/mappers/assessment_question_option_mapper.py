from apps.assessment.domain.entities.assessment_question_option_entity import (
    AssessmentQuestionOption,
)

from apps.assessment.infrastructure.persistence.models.assessment_question_option_model import (
    AssessmentQuestionOptionModel,
)


class AssessmentQuestionOptionMapper:

    @staticmethod
    def to_model(
        entity: AssessmentQuestionOption,
    ) -> AssessmentQuestionOptionModel:

        return AssessmentQuestionOptionModel(
            option_id=entity.option_id,
            content=entity.content,
            order=entity.order,
        )

    @staticmethod
    def to_entity(
        model: AssessmentQuestionOptionModel,
    ) -> AssessmentQuestionOption:

        return AssessmentQuestionOption(
            option_id=model.option_id,
            content=model.content,
            order=model.order,
        )