class StudentClassSectionDTO {
  constructor({
    classSectionId,
    academicYearId,
    semesterId,
    subjectId,
    groupNumber,
    subjectName,
    teacherName,
  }) {
    this.classSectionId = classSectionId;
    this.academicYearId = academicYearId;
    this.semesterId = semesterId;
    this.subjectId = subjectId;
    this.groupNumber = groupNumber;
    this.subjectName = subjectName;
    this.teacherName = teacherName;
  }

  static fromResponse(data) {
    return new StudentClassSectionDTO({
      classSectionId: data.class_section_id,
      academicYearId: data.academic_year_id,
      semesterId: data.semester_id,
      subjectId: data.subject_id,
      groupNumber: data.group_number,
      subjectName: data.subject_name,
      teacherName: data.teacher_name,
    });
  }
}

module.exports = StudentClassSectionDTO;