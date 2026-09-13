const {
  importClassSectionStudentsUseCase,

  getClassSectionStudentsUseCase,

} = require(
  "../../../application/class_sections/dependencies/class_section_student_dependency"
);


const classSectionStudentController = {

  async importStudents(
    req,
    res,
    next
  ) {

    try {

      const file =
        req.file;

      const result =
        await importClassSectionStudentsUseCase
          .execute(
            req,
            file
          );

      return res.status(
        200
      ).json({
        success: true,

        data: result,
      });

    } catch (error) {

      next(error);
    }
  },


  async getStudents(
    req,
    res,
    next
  ) {

    try {

      const result =
        await getClassSectionStudentsUseCase
          .execute(
            req,
            {
              academicYearId:
                req.query.academic_year_id,

              semesterId:
                req.query.semester_id,

              subjectId:
                req.query.subject_id,

              groupNumber:
                req.query.group_number,
            }
          );

      return res.status(
        200
      ).json({
        success: true,

        data: result,
      });

    } catch (error) {

      next(error);
    }
  },

};


module.exports =
  classSectionStudentController;