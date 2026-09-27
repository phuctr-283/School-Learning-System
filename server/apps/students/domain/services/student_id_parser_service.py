class StudentIdParserService:

    PREFIX = "DH"

    @classmethod
    def parse(cls, student_id: str):

        student_id = student_id.strip().upper()

        if not student_id.startswith(cls.PREFIX):
            raise ValueError(
                "MSSV phải bắt đầu bằng DH."
            )

        if len(student_id) != 10:
            raise ValueError(
                "MSSV phải có đúng 10 ký tự."
            )

        number_part = student_id[2:]

        if not number_part.isdigit():
            raise ValueError(
                "MSSV không hợp lệ."
            )

        # =========================================
        # Khoa 1 chữ số
        # X + XX + XXXXX
        # =========================================

        if "1" <= number_part[0] <= "9":

            department_candidates = [
                number_part[0]
            ]

            cohort_id = number_part[1:3]

            sequence = number_part[3:]

        # =========================================
        # Khoa 2 chữ số
        # 0X + XX + XXXX
        # =========================================

        else:

            department_number = number_part[0:2]

            if department_number == "00":
                raise ValueError(
                    "Mã khoa không hợp lệ."
                )

            department_candidates = [
                department_number,
                department_number.lstrip("0"),
            ]

            cohort_id = number_part[2:4]

            sequence = number_part[4:]

        if not cohort_id.isdigit():
            raise ValueError(
                "Không xác định được khóa từ MSSV."
            )

        return {
            "department_candidates": department_candidates,
            "cohort_id": cohort_id,
            "sequence": sequence,
        }