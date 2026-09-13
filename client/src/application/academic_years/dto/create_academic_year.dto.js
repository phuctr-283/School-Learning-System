class CreateAcademicYearDTO {
  constructor({ name, start_date, end_date }) {
    this.name = name?.trim();

    this.startDate = start_date;

    this.endDate = end_date;
  }

  toJSON() {
    return {
      name: this.name,

      start_date: this.startDate,

      end_date: this.endDate,
    };
  }
}

module.exports = CreateAcademicYearDTO;
