class ClassSectionLessonPlanIdGenerator:

    PREFIX = "CSLP"

    def generate(
        self,
        subject_id: str,
        group_number: int,
    ) -> str:

        if not subject_id:
            raise ValueError(
                "Subject ID không được để trống."
            )

        if group_number < 1:
            raise ValueError(
                "Group number phải lớn hơn hoặc bằng 1."
            )

        return (
            f"{self.PREFIX}-"
            f"{subject_id}-"
            f"{group_number}"
        )