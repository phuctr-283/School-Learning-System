class CreateSemesterDTO {
  constructor(data = {}) {
    this.academicYearId = data.academic_year_id;

    this.semesterNumber = data.semester_number;

    this.startDate = data.start_date;

    this.endDate = data.end_date;
  }

  toJSON() {
    return {
      academic_year_id: this.academicYearId,

      semester_number: this.semesterNumber,

      start_date: this.startDate,

      end_date: this.endDate,
    };
  }
}

module.exports = CreateSemesterDTO;
