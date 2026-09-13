from mongoengine import (
    EmbeddedDocument,
    StringField,
    DecimalField,
    BooleanField,
)


class AssignmentAttemptAnswerModel(
    EmbeddedDocument
):

    question_id = StringField(
        required=True,
        max_length=30,
    )

    answer = StringField(
        required=False,
        null=True,
    )

    score = DecimalField(
        required=False,
        null=True,
        precision=2,
    )

    is_correct = BooleanField(
        required=False,
        null=True,
    )