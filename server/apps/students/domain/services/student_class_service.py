class StudentClassService:

    @staticmethod
    def get_cohort_from_class(
        student_class: str,
    ):

        student_class = (
            student_class
            .strip()
            .upper()
        )

        parts = student_class.split("_")

        if len(parts) < 2:
            raise ValueError(
                "Lớp sinh viên không đúng định dạng. "
                "Ví dụ: D23_TH09."
            )

        cohort_part = parts[0]

        if not cohort_part.startswith("D"):
            raise ValueError(
                "Lớp sinh viên phải bắt đầu bằng mã khóa. "
                "Ví dụ: D23_TH09."
            )

        cohort_id = cohort_part[1:]

        if not cohort_id.isdigit():
            raise ValueError(
                "Không xác định được khóa từ lớp sinh viên."
            )

        return cohort_id

    @classmethod
    def validate_cohort(
        cls,
        student_class: str,
        cohort_id: str,
    ):

        class_cohort_id = (
            cls.get_cohort_from_class(
                student_class
            )
        )

        if class_cohort_id != cohort_id:
            raise ValueError(
                f"Lớp {student_class} không thuộc "
                f"khóa {cohort_id} theo MSSV."
            )

        return True