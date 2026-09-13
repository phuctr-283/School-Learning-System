class ClassSectionDTO {
  constructor(data = {}) {
    this.classSectionId = data.class_section_id;

    this.subjectId = data.subject_id;

    this.subjectName = data.subject_name;

    this.groupNumber = data.group_number;

    this.teacherId = data.teacher_id;

    this.teacherName = data.teacher_name;

    this.semesterId = data.semester_id;

    this.semesterName = data.semester_name;

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

module.exports = ClassSectionDTO;
