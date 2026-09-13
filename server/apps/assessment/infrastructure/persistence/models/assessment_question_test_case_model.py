from mongoengine import (
    EmbeddedDocument,
    StringField,
    BooleanField,
    IntField,
)


class AssessmentQuestionTestCaseModel(
    EmbeddedDocument
):

    test_case_id = StringField(
        required=True,
        max_length=30,
    )

    input = StringField(
        required=False,
        null=True,
    )

    expected_output = StringField(
        required=True,
    )

    is_hidden = BooleanField(
        default=True,
    )

    order = IntField(
        required=True,
        min_value=1,
    )