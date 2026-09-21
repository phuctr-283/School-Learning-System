from decimal import Decimal
from mongoengine import (
    EmbeddedDocument,
    EmbeddedDocumentListField,
    EmbeddedDocumentField,
    StringField,
    DecimalField,
    IntField,
    BooleanField,
)

from .assessment_question_option_model import (
    AssessmentQuestionOptionModel,
)

from .assessment_question_answer_model import (
    AssessmentQuestionAnswerModel,
)

from .assessment_question_test_case_model import (
    AssessmentQuestionTestCaseModel,
)


class AssessmentQuestionModel(EmbeddedDocument):

    question_id = StringField(
        required=True,
        max_length=30,
    )
    question = StringField(required = True)

    content = StringField(
        required=False,
        null= True,
        default="",
    )

    question_type = StringField(
        required=True,
        choices=[
            "multiple_choice",
            # "true_false",
            # "short_answer",
            # "essay",
            # "code",
            "ordering",
            "drag_and_drop",
        ],
    )

    score = DecimalField(
        required=True,
        precision=2,
        min_value=Decimal("0.01"),
        max_value=Decimal("10.00"),
    )

    order = IntField(
        required=True,
        min_value=1,
    )

    shuffle_options = BooleanField(
        required=True,
        default=False,
    )
    blank_count = IntField(
        required=True,
        min_value=0,
        default=0,
    )

    options = EmbeddedDocumentListField(
        AssessmentQuestionOptionModel,
        default=list,
    )

    answer = EmbeddedDocumentField(
        AssessmentQuestionAnswerModel,
        required=False,
        null=True,
    )

    test_cases = EmbeddedDocumentListField(
        AssessmentQuestionTestCaseModel,
        default=list,
    )
