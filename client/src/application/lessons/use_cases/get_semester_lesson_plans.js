class GetSemesterLessonPlansUseCase {

    constructor(
        semesterLessonPlanRepository,
    ) {

        this.semesterLessonPlanRepository =
            semesterLessonPlanRepository;
    }


    async execute(req) {

        return await this.semesterLessonPlanRepository
            .getSemesterLessonPlans(req);
    }
}


module.exports =
    GetSemesterLessonPlansUseCase;