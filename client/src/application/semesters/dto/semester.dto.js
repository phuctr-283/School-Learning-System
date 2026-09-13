class SemesterDTO {
  constructor(data = {}) {
    this.semesterId = data.semester_id;
    this.name = data.name;
    this.semesterNumber = data.semester_number;

    this.academicYearId = data.academic_year_id;
    this.academicYearName = data.academic_year_name;

    this.universityId = data.university_id;
    this.universityName = data.university_name;

    this.startDate = data.start_date;
    this.endDate = data.end_date;

    this.status = data.status;
  }
}

module.exports = SemesterDTO;
