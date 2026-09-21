from apps.students.application.dto.import_student_dto import (
    ImportStudentDTO,
)

from apps.students.application.dto.validated_student_dto import (
    ValidatedStudent,
)

from apps.students.domain.entities.student_entity import (
    Student,
)

from apps.students.domain.services.student_id_parser_service import (
    StudentIdParserService,
)

from apps.students.domain.services.student_class_service import (
    StudentClassService,
)

from apps.users.domain.enums.account_level import (
    AccountLevel,
)
from apps.users.application.dto.user_dto import CreateUserDTO


class ImportStudentsUseCase:

    def __init__(
        self,
        student_repository,
        university_repository,
        department_repository,
        user_repository,
        create_user_use_case,
    ):

        self.student_repository = student_repository

        self.university_repository = university_repository

        self.department_repository = department_repository

        self.user_repository = user_repository

        self.create_user_use_case = create_user_use_case

    def execute(
        self,
        rows,
        university_id: str,
    ):

        # =========================================
        # University
        # =========================================

        university = self.university_repository.find_by_id(university_id)

        if not university:

            raise ValueError("Không tìm thấy trường.")

        validated_students = []

        errors = []

        file_student_ids = set()

        file_emails = set()

        # =========================================
        # PHASE 1
        # VALIDATE
        # =========================================

        for row in rows:

            row_number = row["row_number"]

            try:

                dto = ImportStudentDTO(
                    student_id=row["MSSV"],
                    full_name=row["Họ và tên"],
                    gender=row["Giới tính"],
                    email=row["Email"],
                    student_class=row["Lớp"],
                )

                # =================================
                # Required
                # =================================

                self._validate_required(dto)

                # =================================
                # MSSV
                # =================================

                parsed = StudentIdParserService.parse(dto.student_id)

                department_candidates = parsed["department_candidates"]

                cohort_id = parsed["cohort_id"]

                # =================================
                # Lớp ↔ Cohort
                # =================================

                StudentClassService.validate_cohort(
                    student_class=dto.student_class,
                    cohort_id=cohort_id,
                )

                # =================================
                # Gender
                # =================================

                gender = self._parse_gender(dto.gender)

                # =================================
                # Duplicate trong file
                # =================================

                student_id = dto.student_id.strip().upper()

                email = dto.email.strip().lower()

                if student_id in file_student_ids:

                    raise ValueError("MSSV bị trùng trong file.")

                if email in file_emails:

                    raise ValueError("Email bị trùng trong file.")

                file_student_ids.add(student_id)

                file_emails.add(email)

                # =================================
                # Department
                # =================================

                department = None
                matched_department_number = None

                for candidate in department_candidates:

                    department = self.department_repository.find_by_number(
                        university_id=university_id,
                        department_number=candidate,
                    )

                    if department:
                        matched_department_number = department.department_number
                        break

                if department is None:
                    candidates_text = ", ".join(department_candidates)

                    raise ValueError(
                        f"Không tìm thấy khoa tương ứng với "
                        f"mã khoa {candidates_text}."
                    )

                # =================================
                # Student ID DB
                # =================================

                if self.student_repository.exists_by_student_id(
                    university_id=university_id,
                    student_id=student_id,
                ):

                    raise ValueError(f"MSSV {student_id} " f"đã tồn tại.")

                # =================================
                # Email DB
                # =================================

                if self.student_repository.exists_by_email(
                    university_id=university_id,
                    email=email,
                ):

                    raise ValueError(f"Email {email} " f"đã tồn tại.")

                # =================================
                # User
                # =================================

                existing_user = self.user_repository.find_by_username(student_id)

                if existing_user:

                    raise ValueError(f"Tài khoản của MSSV " f"{student_id} đã tồn tại.")

                # =================================
                # Validated
                # =================================

                validated_students.append(
                    ValidatedStudent(
                        row_number=row_number,
                        student_id=student_id,
                        full_name=(dto.full_name.strip()),
                        gender=gender,
                        email=email,
                        student_class=(dto.student_class.strip().upper()),
                        department_number=matched_department_number,
                        cohort_id=cohort_id,
                        department=department,
                    )
                )

            except ValueError as error:

                errors.append(f"Dòng {row_number}: " f"{str(error)}")

        # =========================================
        # Nếu có lỗi → không tạo gì
        # =========================================

        if errors:

            raise ValueError("\n".join(errors))

        # =========================================
        # PHASE 2
        # CREATE
        # =========================================

        created_count = 0

        for item in validated_students:

            # -------------------------------
            # Create Student Entity
            # -------------------------------

            student = Student(
                student_id=item.student_id,
                full_name=item.full_name,
                gender=item.gender,
                student_class=item.student_class,
                department_id=(item.department.department_id),
                department_name=(item.department.name),
                cohort_id=item.cohort_id,
                status="studying",
                university_id=(university.university_id),
                university_name=(university.name),
                date_of_birth=None,
                email=item.email,
                phone=None,
            )

            # -------------------------------
            # Create Student
            # -------------------------------

            self.student_repository.create(
                student=student,
                university=university,
                department=item.department,
            )

            # -------------------------------
            # Create User
            # -------------------------------

            self.create_user_use_case.execute(
                CreateUserDTO(
                    user_id=None,
                    username=item.student_id,
                    password=item.student_id,
                    account_level=(AccountLevel.STUDENT),
                    university_id=(university.university_id),
                )
            )

            created_count += 1

        return {
            "created_count": created_count,
            "skipped_count": 0,
        }

    # =========================================
    # Helpers
    # =========================================

    @staticmethod
    def _validate_required(dto):

        if not dto.student_id:
            raise ValueError("MSSV không được để trống.")

        if not dto.full_name:
            raise ValueError("Họ tên không được để trống.")

        if not dto.gender:
            raise ValueError("Giới tính không được để trống.")

        if not dto.email:
            raise ValueError("Email không được để trống.")

        if not dto.student_class:
            raise ValueError("Lớp không được để trống.")

    @staticmethod
    def _parse_gender(value):

        value = value.strip().lower()

        if value in (
            "nam",
            "male",
        ):
            return "male"

        if value in (
            "nữ",
            "nu",
            "female",
        ):
            return "female"

        raise ValueError("Giới tính chỉ được là Nam hoặc Nữ.")
