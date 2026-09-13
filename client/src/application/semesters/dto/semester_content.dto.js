class SemesterContentDTO {
  constructor(data = {}) {
    this.semesterId = data.semester_id ?? data.semesterId;

    this.name = data.name;

    this.semesterNumber = data.semester_number ?? data.semesterNumber;

    this.academicYearId = data.academic_year_id ?? data.academicYearId;

    this.academicYearName = data.academic_year_name ?? data.academicYearName;

    this.universityId = data.university_id ?? data.universityId;

    this.universityName = data.university_name ?? data.universityName;

    this.status = data.status;
  }
}

module.exports = SemesterContentDTO;
