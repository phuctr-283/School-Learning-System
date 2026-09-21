from apps.assessment.domain.entities.assessment_question_entity import (
    AssessmentQuestion,
)

from apps.assessment.infrastructure.persistence.models.assessment_question_model import (
    AssessmentQuestionModel,
)

from apps.assessment.infrastructure.persistence.mappers.assessment_question_option_mapper import (
    AssessmentQuestionOptionMapper,
)

from apps.assessment.infrastructure.persistence.mappers.assessment_question_answer_mapper import (
    AssessmentQuestionAnswerMapper,
)

from apps.assessment.infrastructure.persistence.mappers.assessment_question_test_case_mapper import (
    AssessmentQuestionTestCaseMapper,
)


class AssessmentQuestionMapper:

    @staticmethod
    def to_model(
        entity: AssessmentQuestion,
    ) -> AssessmentQuestionModel:

        option_models = [
            AssessmentQuestionOptionMapper.to_model(
                option,
            )
            for option in entity.options
        ]

        answer_model = None

        if entity.answer is not None:
            answer_model = AssessmentQuestionAnswerMapper.to_model(
                entity.answer,
            )

        test_case_models = [
            AssessmentQuestionTestCaseMapper.to_model(
                test_case,
            )
            for test_case in entity.test_cases
        ]

        return AssessmentQuestionModel(
            question_id=entity.question_id,
            question=entity.question,
            content=entity.content,
            question_type=entity.question_type,
            score=entity.score,
            order=entity.order,
            shuffle_options=entity.shuffle_options,
            blank_count=entity.blank_count,
            options=option_models,
            answer=answer_model,
            test_cases=test_case_models,
        )

    @staticmethod
    def to_entity(
        model: AssessmentQuestionModel,
    ) -> AssessmentQuestion:

        options = [
            AssessmentQuestionOptionMapper.to_entity(
                option_model,
            )
            for option_model in (model.options or [])
        ]

        answer = None

        if model.answer is not None:
            answer = AssessmentQuestionAnswerMapper.to_entity(
                model.answer,
            )

        test_cases = [
            AssessmentQuestionTestCaseMapper.to_entity(
                test_case_model,
            )
            for test_case_model in (model.test_cases or [])
        ]

        return AssessmentQuestion(
            question_id=model.question_id,
            question=model.question,
            content=model.content,
            question_type=model.question_type,
            score=model.score,
            order=model.order,
            shuffle_options=model.shuffle_options,
            blank_count=model.blank_count,
            options=options,
            answer=answer,
            test_cases=test_cases,
        )
