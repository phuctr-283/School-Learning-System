class ClassSectionStudentRepository {

  async importStudents(
    req,
    file
  ) {

    throw new Error(
      "importStudents() must be implemented"
    );
  }

  async getStudents(
    req,
    params
  ) {

    throw new Error(
      "getStudents() must be implemented"
    );
  }
}

module.exports =
  ClassSectionStudentRepository;