from apps.semesters.domain.entities.semester_entity import (
    Semester,
)

from apps.semesters.domain.services.semester_status_service import (
    SemesterStatusService,
)


class CreateSemesterUseCase:

    def __init__(
        self,
        semester_repository,
        academic_year_repository,
        update_semester_statuses_use_case,
    ):

        self.semester_repository = (
            semester_repository
        )

        self.academic_year_repository = (
            academic_year_repository
        )

        self.update_semester_statuses_use_case = (
            update_semester_statuses_use_case
        )

    def execute(
        self,
        data,
        university_id: str,
    ):

        # =====================================================
        # VALIDATE SEMESTER NUMBER
        # =====================================================

        if data.semester_number not in [
            "1",
            "2",
            "3",
        ]:

            raise ValueError(
                "Học kỳ không hợp lệ."
            )

        # =====================================================
        # GET ACADEMIC YEAR MODEL
        # =====================================================

        academic_year = (
            self.academic_year_repository
            .get_academic_year_by_id(
                university_id=university_id,
                academic_year_id=data.academic_year_id,
            )
        )

        if not academic_year:

            raise ValueError(
                "Không tìm thấy năm học."
            )

        # =====================================================
        # VALIDATE DATE
        # =====================================================

        if not data.start_date:

            raise ValueError(
                "Ngày bắt đầu không được để trống."
            )

        if not data.end_date:

            raise ValueError(
                "Ngày kết thúc không được để trống."
            )

        if data.start_date >= data.end_date:

            raise ValueError(
                "Ngày bắt đầu phải trước ngày kết thúc."
            )

        # =====================================================
        # VALIDATE SEMESTER DUPLICATE
        # =====================================================

        exists = (
            self.semester_repository
            .exists_by_number(
                academic_year_id=(
                    data.academic_year_id
                ),
                semester_number=(
                    data.semester_number
                ),
            )
        )

        if exists:

            raise ValueError(
                f"Học kỳ {data.semester_number} "
                f"đã tồn tại trong năm học "
                f"{academic_year.name}."
            )

        # =====================================================
        # GET START YEAR
        # =====================================================

        start_year = (
            academic_year.start_date.year
        )

        # =====================================================
        # GENERATE SEMESTER ID
        #
        # 2025-2026 + 1 => 20251
        # 2025-2026 + 2 => 20252
        # 2025-2026 + 3 => 20253
        # =====================================================

        semester_id = (
            f"{start_year}"
            f"{data.semester_number}"
        )

        # =====================================================
        # GENERATE NAME
        # =====================================================

        name = (
            f"Học kỳ "
            f"{data.semester_number}"
        )

        # =====================================================
        # CALCULATE STATUS
        # =====================================================

        status = SemesterStatusService.calculate(
            start_date=data.start_date,
            end_date=data.end_date,
        )

        # =====================================================
        # CREATE ENTITY
        # =====================================================

        semester = Semester(
            semester_id=semester_id,
            name=name,
            semester_number=data.semester_number,

            academic_year_id=(
                academic_year.academic_year_id
            ),

            academic_year_name=(
                academic_year.name
            ),

            university_id=(
                academic_year.university.university_id
            ),

            university_name=(
                academic_year.university.name
            ),

            start_date=data.start_date,
            end_date=data.end_date,
            status=status,
        )

        # =====================================================
        # SAVE
        # =====================================================

        semester = (
            self.semester_repository.create(
                semester=semester,
                academic_year=academic_year,
            )
        )

        # =====================================================
        # UPDATE SEMESTER STATUS
        # =====================================================

        self.update_semester_statuses_use_case.execute(
            university_id=university_id,
        )

        return semester