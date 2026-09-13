class LessonDTO {

    constructor(data = {}) {

        this.lessonId =
            data.lesson_id;

        this.lessonNumber =
            data.lesson_number;

        this.name =
            data.name;

        this.universityId =
            data.university_id;
    }
}

module.exports = LessonDTO;