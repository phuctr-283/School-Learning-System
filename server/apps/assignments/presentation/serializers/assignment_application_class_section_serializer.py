from rest_framework import serializers
class AssignmentApplicationClassSectionSerializer(
    serializers.Serializer
):

    class_section_id = serializers.CharField()

    status = serializers.ChoiceField(
        choices=[
            "active",
            "closed",
        ]
    )

    opened_at = serializers.DateTimeField(
        allow_null=True,
        required=False,
    )

    closed_at = serializers.DateTimeField(
        allow_null=True,
        required=False,
    )