from decimal import Decimal
from mongoengine import (
    EmbeddedDocument,
    EmbeddedDocumentListField,
    EmbeddedDocumentField,
    StringField,
    DecimalField,
    IntField,
    BooleanField
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


class AssessmentQuestionModel(
    EmbeddedDocument
):

    # =========================================
    # IDENTIFICATION
    # =========================================

    question_id = StringField(
        required=True,
        max_length=30,
    )

    # =========================================
    # CONTENT
    # =========================================

    content = StringField(
        required=True,
    )

    # =========================================
    # TYPE
    # =========================================

    question_type = StringField(
        required=True,
        choices=[
            "multiple_choice",
            #"true_false",
            #"short_answer",
            #"essay",
            #"code",
            "ordering",
            "drag_and_drop",
        ],
    )

    # =========================================
    # SCORE
    # =========================================

    score = DecimalField(
    required=True,
    precision=2,
    min_value=Decimal("0.01"),
    max_value=Decimal("10.00"),
)

    # =========================================
    # ORDER
    # =========================================

    order = IntField(
        required=True,
        min_value=1,
    )
    # =========================================
    # SHUFFLE
    # =========================================

    shuffle_options = BooleanField(
        required=True,
        default=False,
    )
    blank_count = IntField(
        required=True,
        min_value=0,
        default=0,
    )
    # =========================================
    # OPTIONS
    # =========================================

    options = EmbeddedDocumentListField(
        AssessmentQuestionOptionModel,
        default=list,
    )

    # =========================================
    # ANSWER
    # =========================================

    answer = EmbeddedDocumentField(
        AssessmentQuestionAnswerModel,
        required=False,
        null=True,
    )

    # =========================================
    # TEST CASES
    # =========================================

    test_cases = EmbeddedDocumentListField(
        AssessmentQuestionTestCaseModel,
        default=list,
    )