class StudentImportNotFoundDTO {
  constructor({
    student_id,
    full_name,
    student_class,
  }) {
    this.studentId = student_id;
    this.fullName = full_name;
    this.studentClass = student_class;
  }
}


class StudentImportResultDTO {
  constructor({
    message,
    subject_name,
    group_number,
    semester_number,
    academic_year_name,
    imported_count,
    skipped_count,
    not_found_count,
    imported,
    skipped,
    not_found,
  }) {
    this.message = message;

    this.subjectName = subject_name;

    this.groupNumber = group_number;

    this.semesterNumber = semester_number;

    this.academicYearName =
      academic_year_name;

    this.importedCount =
      imported_count;

    this.skippedCount =
      skipped_count;

    this.notFoundCount =
      not_found_count;

    this.imported =
      imported || [];

    this.skipped =
      skipped || [];

    this.notFound = (
      not_found || []
    ).map(
      item =>
        new StudentImportNotFoundDTO(
          item
        )
    );
  }

  static fromResponse(data) {
    return new StudentImportResultDTO(
      data
    );
  }
}

module.exports =
  StudentImportResultDTO;