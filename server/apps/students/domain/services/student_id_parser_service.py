class StudentIdParserService:

    PREFIX = "DH"

    @classmethod
    def parse(
        cls,
        student_id: str,
    ):

        student_id = student_id.strip().upper()

        # =========================================
        # Prefix
        # =========================================

        if not student_id.startswith(cls.PREFIX):

            raise ValueError("MSSV phải bắt đầu bằng DH.")

        # =========================================
        # Length
        # =========================================

        if len(student_id) not in (
            10,
            11,
        ):

            raise ValueError("MSSV phải có 10 hoặc 11 ký tự.")

        number_part = student_id[2:]

        if not number_part.isdigit():

            raise ValueError("MSSV không hợp lệ.")

        # =========================================
        # 10 characters
        #
        # DH52301555
        #   │
        #   ├── 5   = department
        #   ├── 23  = cohort
        #   └── 01555 = sequence
        # =========================================

        if len(student_id) == 10:

            department_number = number_part[0].zfill(2)

            cohort_id = number_part[1:3]

            sequence = number_part[3:]

        # =========================================
        # 11 characters
        #
        # DH052301555
        #   │
        #   ├── 05  = department
        #   ├── 23  = cohort
        #   └── 01555 = sequence
        # =========================================

        else:

            department_number = number_part[0:2]

            cohort_id = number_part[2:4]

            sequence = number_part[4:]

        # =========================================
        # Validate
        # =========================================

        if not department_number:

            raise ValueError("Không xác định được mã khoa từ MSSV.")

        if not cohort_id:

            raise ValueError("Không xác định được khóa từ MSSV.")

        if len(sequence) != 5:

            raise ValueError("Phần số thứ tự MSSV không hợp lệ.")

        return {
            "department_number": department_number,
            "cohort_id": cohort_id,
        }
