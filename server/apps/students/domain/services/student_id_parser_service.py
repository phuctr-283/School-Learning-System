class StudentIdParserService:

    PREFIX = "DH"

    @classmethod
    def parse(cls, student_id: str):

        student_id = student_id.strip().upper()

        if not student_id.startswith(cls.PREFIX):
            raise ValueError(
                "MSSV phải bắt đầu bằng DH."
            )

        if len(student_id) not in (10, 11):
            raise ValueError(
                "MSSV phải có 10 hoặc 11 ký tự."
            )

        number_part = student_id[2:]

        if not number_part.isdigit():
            raise ValueError(
                "MSSV không hợp lệ."
            )

        if len(student_id) == 10:

            department_candidates = [
                number_part[0],
            ]

            cohort_id = number_part[1:3]
            sequence = number_part[3:]

        else:

            department_candidates = [
                number_part[0:2],
                number_part[0:2].lstrip("0"),
            ]

            cohort_id = number_part[2:4]
            sequence = number_part[4:]

        if not cohort_id or not cohort_id.isdigit():
            raise ValueError(
                "Không xác định được khóa từ MSSV."
            )

        if len(sequence) != 5:
            raise ValueError(
                "Phần số thứ tự MSSV không hợp lệ."
            )

        return {
            "department_candidates": department_candidates,
            "cohort_id": cohort_id,
        }