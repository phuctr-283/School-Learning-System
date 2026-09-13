from rest_framework import serializers


class LessonSerializer(serializers.Serializer):

    lesson_id = serializers.CharField()

    lesson_number = serializers.IntegerField()

    name = serializers.CharField()

    university_id = serializers.CharField()