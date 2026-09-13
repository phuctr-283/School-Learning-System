class SemesterLessonPlanDTO {

    constructor(data = {}) {

        this.semesterLessonPlanId =
            data.semester_lesson_plan_id;

        this.universityId =
            data.university_id;

        this.academicYearId =
            data.academic_year_id;

        this.academicYearName =
            data.academic_year_name;

        this.semesterId =
            data.semester_id;

        this.semesterName =
            data.semester_name;

        this.semesterNumber =
            data.semester_number;

        this.totalLessons =
            data.total_lessons;
    }
}

module.exports = SemesterLessonPlanDTO;