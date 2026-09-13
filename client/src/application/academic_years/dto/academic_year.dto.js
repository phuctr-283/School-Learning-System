class AcademicYearDTO {
  constructor(data = {}) {
    this.academicYearId = data.academic_year_id;
    this.universityId = data.university_id;
    this.universityName = data.university_name;

    this.name = data.name;

    this.startDate = data.start_date;
    this.endDate = data.end_date;

    this.status = data.status;
  }
}

module.exports = AcademicYearDTO;
