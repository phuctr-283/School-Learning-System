from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.infrastructure.persistence.models.user_model import (
    UserModel,
)

from apps.teachers.infrastructure.persistence.models.teacher_model import (
    TeacherModel,
)

from apps.class_sections.presentation.serializers.class_section_student_serializer import (
    ImportClassSectionStudentsSerializer,
)

from apps.class_sections.infrastructure.dependencies.class_section_student_dependency import (
    import_class_section_students_by_teacher_dependency,
)


class ImportClassSectionStudentsByTeacherView(APIView):

    def post(self, request):

        # ==================================================
        # 1. Lấy user_id từ tài khoản đã xác thực
        # ==================================================
        user_id = getattr(
            request.user,
            "user_id",
            None,
        )

        if not user_id:
            return Response(
                {
                    "success": False,
                    "message": "Không xác định được người dùng",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )


        # ==================================================
        # 2. Tìm tài khoản UserModel
        # ==================================================
        user = (
            UserModel.objects(
                user_id=user_id,
                is_active=True,
            )
            .first()
        )

        if not user:
            return Response(
                {
                    "success": False,
                    "message": "Tài khoản không tồn tại",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )


        # ==================================================
        # 3. Lấy username và university_id từ UserModel
        # ==================================================
        username = getattr(
            user,
            "username",
            None,
        )

        university_id = getattr(
            user,
            "university_id",
            None,
        )

        if not username:
            return Response(
                {
                    "success": False,
                    "message": "Tài khoản chưa có username",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not university_id:
            return Response(
                {
                    "success": False,
                    "message": "Tài khoản chưa thuộc trường đại học",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


        # ==================================================
        # 4. Tìm giảng viên bằng email = username
        # ==================================================
        teacher = (
            TeacherModel.objects(
                email=username,
            )
            .first()
        )

        if not teacher:
            return Response(
                {
                    "success": False,
                    "message": (
                        "Không tìm thấy giảng viên tương ứng "
                        "với tài khoản đang đăng nhập"
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )


        # ==================================================
        # 5. Lấy teacher_id từ TeacherModel
        # ==================================================
        teacher_id = getattr(
            teacher,
            "teacher_id",
            None,
        )

        if not teacher_id:
            return Response(
                {
                    "success": False,
                    "message": "Giảng viên chưa có mã giảng viên",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


        # ==================================================
        # 6. Lấy file Excel
        # ==================================================
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return Response(
                {
                    "success": False,
                    "message": "Vui lòng chọn file Excel",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


        # ==================================================
        # 7. Thực hiện import
        # ==================================================
        try:

            result = (
                import_class_section_students_by_teacher_dependency
                .execute(
                    file=uploaded_file,
                    teacher_id=teacher_id,
                    university_id=university_id,
                )
            )


            serializer = ImportClassSectionStudentsSerializer(
                result
            )


            return Response(
                {
                    "success": True,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )


        except ValueError as exc:

            return Response(
                {
                    "success": False,
                    "message": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )