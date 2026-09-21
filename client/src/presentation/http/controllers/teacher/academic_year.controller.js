const{
getActiveAndPlannedAcademicYearsUseCase
} = require("../../../../infrastructure/dependencies/academic_year/academic_year_dependency");

class AcademicYearController{
    async getAcademicYearActivePlanned(req,res){
        try{
            const academicYears = await getActiveAndPlannedAcademicYearsUseCase.execute(req)
        } catch(error){

        }
    }
}

module.exports = new AcademicYearController();