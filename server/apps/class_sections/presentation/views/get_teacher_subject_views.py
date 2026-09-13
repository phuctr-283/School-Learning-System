from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.infrastructure.persistence.models.user_model import (
    UserModel,
)

from apps.teachers.infrastructure.persistence.models.teacher_model import (
    TeacherModel,
)

from apps.class_sections.infrastructure.dependencies.get_teacher_subjects_dependency import (
    get_teacher_subjects_dependency,
)

from apps.class_sections.presentation.serializers.teacher_subject_serializer import (
    TeacherSubjectSerializer,
)


class GetTeacherSubjectsView(APIView):

    def get(self, request):

        # =========================================
        # USER ID
        # =========================================

        user_id = getattr(
            request.user,
            "user_id",
            None,
        )

        if not user_id:
            return Response(
                {
                    "success": False,
                    "message": "Không xác định được tài khoản.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # =========================================
        # USER
        # =========================================

        user = UserModel.objects(
            user_id=user_id,
            is_active=True,
        ).first()

        if not user:
            return Response(
                {
                    "success": False,
                    "message": "Không tìm thấy tài khoản.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # =========================================
        # UNIVERSITY
        # =========================================

        university_id = user.university_id

        if not university_id:
            return Response(
                {
                    "success": False,
                    "message": "Tài khoản không thuộc trường đại học.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # =========================================
        # TEACHER
        #
        # username = teacher.email
        # =========================================

        teacher = TeacherModel.objects(
            email=user.username,
        ).first()

        if not teacher:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Không tìm thấy giảng viên "
                        "tương ứng với tài khoản."
                    ),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # =========================================
        # TEACHER ID
        # =========================================

        if not teacher.teacher_id:
            return Response(
                {
                    "success": False,
                    "message": "Giảng viên chưa có mã giảng viên.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # =========================================
        # DEPARTMENT
        # =========================================

        department = teacher.department

        if not department:
            return Response(
                {
                    "success": False,
                    "message": "Giảng viên chưa thuộc khoa.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # =========================================
        # UNIVERSITY OF DEPARTMENT
        # =========================================

        if not department.university:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Khoa của giảng viên "
                        "chưa thuộc trường đại học."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # =========================================
        # CHECK UNIVERSITY
        # =========================================

        if (
            department.university.university_id
            != university_id
        ):
            return Response(
                {
                    "success": False,
                    "message": (
                        "Giảng viên không thuộc "
                        "trường đại học của tài khoản."
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # =========================================
        # GET TEACHER SUBJECTS
        # =========================================

        try:

            subjects = (
                get_teacher_subjects_dependency
                .execute(
                    university_id=university_id,
                    department_id=department.department_id,
                    teacher_id=teacher.teacher_id,
                )
            )

            serializer = TeacherSubjectSerializer(
                subjects,
                many=True,
            )

            return Response(
                {
                    "success": True,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )