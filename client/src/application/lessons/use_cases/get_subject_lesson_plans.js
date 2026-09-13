class GetSubjectLessonPlansUseCase {

    constructor(
        subjectLessonPlanRepository,
    ) {

        this.subjectLessonPlanRepository =
            subjectLessonPlanRepository;
    }


    async execute(req) {

        return await this.subjectLessonPlanRepository
            .getSubjectLessonPlans(req);
    }
}


module.exports =
    GetSubjectLessonPlansUseCase;