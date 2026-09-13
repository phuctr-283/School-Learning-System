class SemesterLessonPlanIdGenerator:

    PREFIX = "SSLP"

    def generate(
        self,
        semester_id: str,
    ) -> str:

        if not semester_id:
            raise ValueError(
                "Semester ID không được để trống."
            )

        return (
            f"{self.PREFIX}-"
            f"{semester_id}"
        )