from mongoengine import (
    EmbeddedDocument,
    StringField,
    IntField,
)


class AssessmentQuestionOptionModel(
    EmbeddedDocument
):

    option_id = StringField(
        required=True,
        max_length=30,
    )

    content = StringField(
        required=True,
    )

    order = IntField(
        required=True,
        min_value=1,
    )