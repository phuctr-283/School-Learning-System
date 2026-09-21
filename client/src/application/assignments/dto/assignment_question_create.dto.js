class AssignmentQuestionCreateDTO {
  constructor({
    question_type,
    content,
    options = [],
    score = null,
  }) {
    this.questionType = question_type;
    this.content = content;
    this.options = Array.isArray(options) ? options : [];
    this.score = score;
  }

  static fromRequest(data = {}) {
    return new AssignmentQuestionCreateDTO({
      question_type: data.question_type,
      content: data.content,
      options: data.options,
      score: data.score,
    });
  }

  toRequest() {
    const payload = {
      question_type: this.questionType,
      content: this.content,
      options: this.options,
    };

    if (
      this.score !== undefined &&
      this.score !== null &&
      this.score !== ""
    ) {
      payload.score = Number(this.score);
    }

    return payload;
  }
}

module.exports = AssignmentQuestionCreateDTO;