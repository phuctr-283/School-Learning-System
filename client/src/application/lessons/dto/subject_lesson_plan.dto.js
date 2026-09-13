class SubjectLessonPlanDTO {

  constructor(data = {}) {

    this.subjectLessonPlanId =
      data.subject_lesson_plan_id;

    this.universityId =
      data.university_id;

    this.semesterNumber =
      data.semester_number;

    this.lessonType =
      data.lesson_type;

    this.minCredits =
      data.min_credits;

    this.maxCredits =
      data.max_credits;

    this.totalLessons =
      data.total_lessons;

    this.isCustom =
      data.is_custom;
  }
}


module.exports = SubjectLessonPlanDTO;