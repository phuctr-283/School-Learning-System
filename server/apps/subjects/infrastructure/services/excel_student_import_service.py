from datetime import datetime


class ExcelStudentImportService:

    REQUIRED_HEADERS = [
        "MSSV",
        "Họ và tên",
        "Giới tính",
        "Email",
        "Lớp",
    ]

    def read(self, file):

        try:

            import openpyxl

            workbook = openpyxl.load_workbook(
                file,
                data_only=True,
            )

            worksheet = workbook.active

        except Exception:

            raise ValueError("Không thể đọc file Excel.")

        # =========================================
        # Kiểm tra header
        # =========================================

        headers = [cell.value for cell in worksheet[1]]

        normalized_headers = [
            str(header).strip() if header is not None else "" for header in headers
        ]

        if normalized_headers != self.REQUIRED_HEADERS:

            raise ValueError(
                "File Excel không đúng định dạng. "
                "Yêu cầu các cột: "
                "MSSV, Họ và tên, Giới tính, Email, Lớp."
            )

        # =========================================
        # Đọc dữ liệu
        # =========================================

        rows = []

        for row_number, values in enumerate(
            worksheet.iter_rows(
                min_row=2,
                values_only=True,
            ),
            start=2,
        ):

            if all(value is None for value in values):
                continue

            row = dict(
                zip(
                    self.REQUIRED_HEADERS,
                    values,
                )
            )

            rows.append(
                {
                    "row_number": row_number,
                    "MSSV": self._string(row["MSSV"]),
                    "Họ và tên": self._string(row["Họ và tên"]),
                    "Giới tính": self._string(row["Giới tính"]),
                    "Email": self._string(row["Email"]),
                    "Lớp": self._string(row["Lớp"]),
                }
            )

        if not rows:

            raise ValueError("File Excel không có dữ liệu.")

        return rows

    @staticmethod
    def _string(value):

        if value is None:
            return ""

        return str(value).strip()
