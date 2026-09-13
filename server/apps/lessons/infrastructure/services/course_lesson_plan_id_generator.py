class CourseLessonPlanIdGenerator:

    PREFIX = "CLP"

    def generate(
        self,
        subject_id: str,
        semester_id: str,
    ) -> str:

        if not subject_id:
            raise ValueError(
                "Subject ID không được để trống."
            )

        if not semester_id:
            raise ValueError(
                "Semester ID không được để trống."
            )

        return (
            f"{self.PREFIX}-"
            f"{subject_id}-"
            f"{semester_id}"
        )