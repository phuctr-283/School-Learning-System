from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.universities.presentation.serializers.university_serializer import (
    UniversitySerializer,
)

from apps.universities.presentation.dependencies import (
    get_universities_use_case,
)


class GetUniversitiesView(APIView):

    def get(self, request):

        universities = (
            get_universities_use_case.execute()
        )

        data = [
            UniversitySerializer(
                university.__dict__
            ).data
            for university in universities
        ]

        return Response(
            {
                "success": True,
                "data": data,
            },
            status=status.HTTP_200_OK,
        )