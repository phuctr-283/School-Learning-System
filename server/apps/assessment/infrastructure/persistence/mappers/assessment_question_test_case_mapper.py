from apps.assessment.domain.entities.assessment_question_test_case_entity import (
    AssessmentQuestionTestCase,
)

from apps.assessment.infrastructure.persistence.models.assessment_question_test_case_model import (
    AssessmentQuestionTestCaseModel,
)


class AssessmentQuestionTestCaseMapper:

    @staticmethod
    def to_model(
        entity: AssessmentQuestionTestCase,
    ) -> AssessmentQuestionTestCaseModel:

        return AssessmentQuestionTestCaseModel(
            test_case_id=entity.test_case_id,
            input=entity.input,
            expected_output=entity.expected_output,
            is_hidden=entity.is_hidden,
            order=entity.order,
        )

    @staticmethod
    def to_entity(
        model: AssessmentQuestionTestCaseModel,
    ) -> AssessmentQuestionTestCase:

        return AssessmentQuestionTestCase(
            test_case_id=model.test_case_id,
            input=model.input,
            expected_output=model.expected_output,
            is_hidden=model.is_hidden,
            order=model.order,
        )