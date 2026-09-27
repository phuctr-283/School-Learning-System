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


class AssignmentApplicationContentSerializer(
    serializers.Serializer
):

    assignment_application_id = serializers.CharField()

    assignment_id = serializers.CharField()

    university_id = serializers.CharField()

    lesson_id = serializers.CharField()

    class_sections = AssignmentApplicationClassSectionSerializer(
        many=True
    )

    title = serializers.CharField()

    description = serializers.CharField(
        allow_null=True,
        required=False,
        allow_blank=True,
    )

    subject_id = serializers.CharField()

    subject_name = serializers.CharField()

    assignment_type = serializers.CharField()

    total_score = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    duration_minutes = serializers.IntegerField()

    status = serializers.CharField()

    max_attempts = serializers.IntegerField()

    open_at = serializers.DateTimeField(
        allow_null=True,
        required=False,
    )

    due_at = serializers.DateTimeField(
        allow_null=True,
        required=False,
    )

    created_at = serializers.DateTimeField()

    updated_at = serializers.DateTimeField()
class AssignmentApplicationSerializer(
    serializers.Serializer
):

    assignment_application_id = serializers.CharField()
    assignment_id = serializers.CharField()
    university_id = serializers.CharField()
    lesson_id = serializers.CharField()
    class_section_id = serializers.CharField()
    class_section_status = serializers.ChoiceField(
        choices=[
            "active",
            "closed",
        ]
    )
    class_section_opened_at = serializers.DateTimeField(
        allow_null=True,
        required=False,
    )
    class_section_closed_at = serializers.DateTimeField(
        allow_null=True,
        required=False,
    )
    title = serializers.CharField()
    description = serializers.CharField(
        allow_null=True,
        required=False,
        allow_blank=True,
    )
    subject_id = serializers.CharField()
    subject_name = serializers.CharField()
    assignment_type = serializers.CharField()
    total_score = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    duration_minutes = serializers.IntegerField()
    status = serializers.CharField()
    max_attempts = serializers.IntegerField()
    open_at = serializers.DateTimeField(
        allow_null=True,
        required=False,
    )
    due_at = serializers.DateTimeField(
        allow_null=True,
        required=False,
    )
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()