from rest_framework import serializers


class AssignmentListSerializer(serializers.Serializer):
    assignment_id =  serializers.CharField()
    subject_name = serializers.CharField()
    title = serializers.CharField()

    description = serializers.CharField(
        allow_null=True,
        required=False,
        allow_blank=True,
    )

    assignment_type = serializers.CharField()

    total_score = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    status = serializers.CharField()
    is_active = serializers.BooleanField()
    created_at = serializers.DateTimeField()

    def to_representation(self, instance):
        return {
            "assignment_id": instance.assignment_id,
            "subject_name": instance.subject_name,
            "title": instance.title,
            "description": instance.description,
            "assignment_type": instance.assignment_type,
            "total_score": instance.total_score,
            "status": instance.status,
            "is_active": instance.is_active,
            "created_at": instance.created_at,
        }