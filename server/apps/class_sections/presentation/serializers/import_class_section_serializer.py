from rest_framework import serializers


class ImportClassSectionSerializer(serializers.Serializer):

    file = serializers.FileField()

    def validate_file(
        self,
        value,
    ):

        if not value.name.lower().endswith(".xlsx"):

            raise serializers.ValidationError("Chỉ hỗ trợ file .xlsx.")

        max_size = 128 * 1024 * 1024

        if value.size > max_size:

            raise serializers.ValidationError(
                "Dung lượng file không được vượt quá " "128 MiB."
            )

        return value
