from mongoengine import (
    EmbeddedDocument,
    ListField,
    StringField,
)


class AssessmentQuestionAnswerModel(
    EmbeddedDocument
):

    correct_option_ids = ListField(
        field=StringField(
            max_length=30,
        ),
        default=list,
    )
    correct_order_option_ids = ListField(
        field=StringField(
            max_length=30,
        ),
        default=list,
    )
    correct_answers = ListField(
        field=StringField(),
        default=list,
    )