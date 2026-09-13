from datetime import date


class AcademicYearStatusService:

    @staticmethod
    def calculate(
        start_date: date,
        end_date: date,
    ) -> str:

        today = date.today()

        if today < start_date:

            return "planned"

        if start_date <= today <= end_date:

            return "active"

        return "inactive"