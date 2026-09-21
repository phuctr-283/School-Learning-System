from rest_framework import serializers


class ApplyAssignmentSerializer(
    serializers.Serializer
):

    assignment_id = serializers.CharField(
        required=True,
        trim_whitespace=True,
    )

    lesson_id = serializers.CharField(
        required=True,
        trim_whitespace=True,
    )

    class_section_ids = serializers.ListField(
        child=serializers.CharField(
            trim_whitespace=True,
        ),
        required=True,
        allow_empty=False,
    )

    max_attempts = serializers.IntegerField(
        required=False,
        min_value=1,
        default=1,
    )

    def validate_class_section_ids(
        self,
        value,
    ):

        result = []

        for class_section_id in value:

            class_section_id = (
                str(class_section_id).strip()
            )

            if (
                class_section_id
                and class_section_id not in result
            ):
                result.append(
                    class_section_id
                )

        if not result:
            raise serializers.ValidationError(
                "Phải chọn ít nhất một nhóm lớp học phần."
            )

        return result