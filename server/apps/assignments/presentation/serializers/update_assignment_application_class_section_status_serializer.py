from rest_framework import serializers


class UpdateAssignmentApplicationClassSectionStatusSerializer(
    serializers.Serializer
):

    is_active = serializers.BooleanField(
        required=True,
    )