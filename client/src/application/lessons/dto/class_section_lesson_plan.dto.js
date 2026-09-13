class ClassSectionLessonPlanDTO {
  constructor(data = {}) {
    this.classSectionLessonPlanId =
      data.class_section_lesson_plan_id ??
      data.classSectionLessonPlanId;

    this.universityId =
      data.university_id ??
      data.universityId;

    this.universityName =
      data.university_name ??
      data.universityName;

    this.courseLessonPlanId =
      data.course_lesson_plan_id ??
      data.courseLessonPlanId;

    this.classSectionId =
      data.class_section_id ??
      data.classSectionId;

    this.groupNumber =
      data.group_number ??
      data.groupNumber;

    this.subjectId =
      data.subject_id ??
      data.subjectId;

    this.subjectName =
      data.subject_name ??
      data.subjectName;

    this.semesterId =
      data.semester_id ??
      data.semesterId;

    this.semesterName =
      data.semester_name ??
      data.semesterName;

    this.semesterNumber =
      data.semester_number ??
      data.semesterNumber;

    this.academicYearId =
      data.academic_year_id ??
      data.academicYearId;

    this.academicYearName =
      data.academic_year_name ??
      data.academicYearName;

    this.totalLessons =
      data.total_lessons ??
      data.totalLessons;

    this.isCustom =
      data.is_custom ??
      data.isCustom ??
      false;

    this.customTotalLessons =
      data.custom_total_lessons ??
      data.customTotalLessons ??
      null;

    this.effectiveTotalLessons =
      data.effective_total_lessons ??
      data.effectiveTotalLessons ??
      this.customTotalLessons ??
      this.totalLessons;
  }
}

module.exports = ClassSectionLessonPlanDTO;