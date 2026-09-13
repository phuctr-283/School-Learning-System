from datetime import date


class SemesterStatusService:

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

        return "locked"