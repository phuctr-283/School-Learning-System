from rest_framework import serializers


class StudentImportNotFoundSerializer(
    serializers.Serializer
):

    student_id = serializers.CharField()

    full_name = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )

    student_class = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )


class ImportClassSectionStudentsSerializer(
    serializers.Serializer
):

    message = serializers.CharField()

    subject_name = serializers.CharField()

    group_number = serializers.IntegerField()

    semester_number = serializers.IntegerField()

    academic_year_name = serializers.CharField()

    imported_count = serializers.IntegerField()

    skipped_count = serializers.IntegerField()

    not_found_count = serializers.IntegerField()

    imported = serializers.ListField(
        child=serializers.CharField()
    )

    skipped = serializers.ListField(
        child=serializers.CharField()
    )

    not_found = StudentImportNotFoundSerializer(
        many=True
    )