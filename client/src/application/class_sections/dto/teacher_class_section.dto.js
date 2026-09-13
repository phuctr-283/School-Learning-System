class TeacherClassSectionDTO {

  constructor({
    university_id,
    department_id,

    class_section_id,

    academic_year_id,
    academic_year_name,

    semester_id,
    semester_name,
    semester_number,

    subject_id,
    subject_name,

    group_number,

    status,
  }) {

    this.universityId = university_id;
    this.departmentId = department_id;

    this.classSectionId = class_section_id;

    this.academicYearId = academic_year_id;
    this.academicYearName = academic_year_name;

    this.semesterId = semester_id;
    this.semesterName = semester_name;
    this.semesterNumber = semester_number;

    this.subjectId = subject_id;
    this.subjectName = subject_name;

    this.groupNumber = group_number;

    this.status = status;
  }


  static fromResponse(data) {

    return new TeacherClassSectionDTO(data);
  }

}


module.exports = TeacherClassSectionDTO;