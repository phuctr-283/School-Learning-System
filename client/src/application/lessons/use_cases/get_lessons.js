class GetLessonsUseCase {

    constructor(lessonRepository) {

        this.lessonRepository =
            lessonRepository;
    }


    async execute(req) {

        return await this.lessonRepository.getLessons(
            req,
        );
    }
}


module.exports = GetLessonsUseCase;