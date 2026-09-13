class CourseLessonPlanDTO {
  constructor(data = {}) {
    this.courseLessonPlanId =
      data.course_lesson_plan_id ?? data.courseLessonPlanId;

    this.universityId = data.university_id ?? data.universityId;

    this.universityName = data.university_name ?? data.universityName;

    this.subjectId = data.subject_id ?? data.subjectId;

    this.subjectName = data.subject_name ?? data.subjectName;

    this.semesterId = data.semester_id ?? data.semesterId;

    this.semesterName = data.semester_name ?? data.semesterName;

    this.semesterNumber = data.semester_number ?? data.semesterNumber;

    this.academicYearId = data.academic_year_id ?? data.academicYearId;

    this.academicYearName = data.academic_year_name ?? data.academicYearName;

    this.totalLessons = data.total_lessons ?? data.totalLessons;
  }
}

module.exports = CourseLessonPlanDTO;
