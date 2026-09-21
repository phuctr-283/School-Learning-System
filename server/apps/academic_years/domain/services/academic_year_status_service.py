from datetime import date

from django.utils import timezone


class AcademicYearStatusService:

    @staticmethod
    def calculate(
        start_date: date,
        end_date: date,
    ) -> str:

        today = timezone.localdate()

        if today < start_date:
            return "planned"

        if today > end_date:
            return "inactive"

        return "active"