class ClassSectionLessonPlanIdGenerator:

    PREFIX = "CSLP"

    def generate(
        self,
        class_section_id: str,
    ) -> str:

        if not class_section_id:
            raise ValueError(
                "Class section ID không được để trống."
            )

        return (
            f"{self.PREFIX}-"
            f"{class_section_id}"
        )