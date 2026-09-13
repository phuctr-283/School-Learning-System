class ImportClassSectionStudentsUseCase {

  constructor(
    classSectionStudentRepository
  ) {

    this.classSectionStudentRepository =
      classSectionStudentRepository;
  }


  async execute(
    req,
    file
  ) {

    if (!file) {

      throw new Error(
        "Vui lòng chọn file Excel"
      );
    }

    return (
      await this
        .classSectionStudentRepository
        .importStudents(
          req,
          file
        )
    );
  }

}


module.exports =
  ImportClassSectionStudentsUseCase;