import re

from apps.academic_years.domain.entities.academic_year_entity import (
    AcademicYear,
)

from apps.academic_years.application.dto.create_academic_year_dto import (
    CreateAcademicYearDTO,
)

from apps.academic_years.domain.services.academic_year_status_service import (
    AcademicYearStatusService,
)


class CreateAcademicYearUseCase:

    def __init__(
        self,
        academic_year_repository,
        university_repository,
        update_academic_year_statuses_use_case,
    ):

        self.academic_year_repository = academic_year_repository

        self.university_repository = university_repository

        self.update_academic_year_statuses_use_case = (
            update_academic_year_statuses_use_case
        )

    def execute(
        self,
        data: CreateAcademicYearDTO,
        university_id: str,
    ):

        # =================================================
        # NORMALIZE
        # =================================================

        name = data.name.strip()

        # =================================================
        # VALIDATE NAME
        # =================================================

        if not name:

            raise ValueError("Tên năm học không được để trống")

        if not re.fullmatch(
            r"\d{4}-\d{4}",
            name,
        ):

            raise ValueError("Tên năm học phải có dạng YYYY-YYYY")

        start_year = int(name[:4])

        end_year = int(name[5:])

        if end_year != start_year + 1:

            raise ValueError("Năm học phải kéo dài đúng một năm")

        # =================================================
        # VALIDATE DATE
        # =================================================

        if not data.start_date:

            raise ValueError("Ngày bắt đầu không được để trống")

        if not data.end_date:

            raise ValueError("Ngày kết thúc không được để trống")

        if data.start_date >= data.end_date:

            raise ValueError("Ngày kết thúc phải lớn hơn ngày bắt đầu")

        # =================================================
        # DATE YEAR
        # =================================================

        if data.start_date.year != start_year:

            raise ValueError(
                "Năm của ngày bắt đầu phải trùng với năm bắt đầu của tên năm học"
            )

        if data.end_date.year != end_year:

            raise ValueError(
                "Năm của ngày kết thúc phải trùng với năm kết thúc của tên năm học"
            )

        # =================================================
        # UNIVERSITY
        # =================================================

        university = self.university_repository.find_by_id(
            university_id,
        )

        if not university:

            raise ValueError("Không tìm thấy trường đại học")

        # =================================================
        # DUPLICATE
        # =================================================

        exists = self.academic_year_repository.exists_by_name(
            university=university,
            name=name,
        )

        if exists:

            raise ValueError(f"Năm học {name} đã tồn tại")

        # =================================================
        # ID
        # =================================================

        academic_year_id = str(start_year)

        # =================================================
        # STATUS
        # =================================================

        status = AcademicYearStatusService.calculate(
            start_date=data.start_date,
            end_date=data.end_date,
        )

        # =================================================
        # ENTITY
        # =================================================

        academic_year = AcademicYear(
            academic_year_id=academic_year_id,
            university_id=(university.university_id),
            university_name=(university.name),
            name=name,
            start_date=data.start_date,
            end_date=data.end_date,
            status=status,
        )

        # =================================================
        # CREATE
        # =================================================

        created_academic_year = self.academic_year_repository.create(
            academic_year=academic_year,
            university=university,
        )

        # =================================================
        # UPDATE ALL STATUS
        # =================================================

        self.update_academic_year_statuses_use_case.execute(
            university_id=university_id,
        )

        return created_academic_year
