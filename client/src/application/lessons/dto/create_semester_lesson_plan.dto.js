class CreateSemesterLessonPlanItemDTO {
  constructor(data = {}) {
    this.semesterNumber = data.semesterNumber;

    this.totalLessons = data.totalLessons;
  }

  toJSON() {
    return {
      semester_number: this.semesterNumber,

      total_lessons: this.totalLessons,
    };
  }
}

class CreateSemesterLessonPlanDTO {

  constructor(data = {}) {
    this.academicYearId = data.academicYearId;

    this.semesters = data.semesters || [];
  }

  static fromRequestBody(body = {}) {
    const semesters = Object.values(body.semesters || {})
      .filter(
        (item) =>
          item && item.total_lessons !== undefined && item.total_lessons !== "",
      )
      .map(
        (item) =>
          new CreateSemesterLessonPlanItemDTO({
            semesterNumber: String(item.semester_number),

            totalLessons: Number(item.total_lessons),
          }),
      );

    return new CreateSemesterLessonPlanDTO({
      academicYearId: body.academic_year_id,

      semesters,
    });
  }

  toJSON() {
    return {
      academic_year_id: this.academicYearId,

      semesters: this.semesters.map((semester) => semester.toJSON()),
    };
  }
}

module.exports = CreateSemesterLessonPlanDTO;
