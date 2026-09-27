class AssignmentHistoryOptionDTO {
  constructor({
    optionId,
    content,
    isCorrect,
    isSelected,
    isSelectedCorrect,
    isSelectedWrong,
  }) {
    this.optionId = optionId;
    this.content = content;
    this.isCorrect = Boolean(isCorrect);
    this.isSelected = Boolean(isSelected);
    this.isSelectedCorrect = Boolean(isSelectedCorrect);
    this.isSelectedWrong = Boolean(isSelectedWrong);
  }
}

class AssignmentHistoryQuestionDTO {
  constructor({
    questionId,
    question,
    content,
    questionType,
    score,
    earnedScore,
    userAnswer,
    correctAnswer,
    correct,
    options,
    correctOptions,
    wrongOptions,
  }) {
    this.questionId = questionId;
    this.question = question;
    this.content = content;
    this.questionType = questionType;
    this.score = score;
    this.earnedScore = earnedScore;
    this.userAnswer = userAnswer;
    this.correctAnswer = correctAnswer;
    this.correct = Boolean(correct);
    this.options = options || [];
    this.correctOptions = correctOptions || [];
    this.wrongOptions = wrongOptions || [];
    this.answered =
      userAnswer !== null &&
      userAnswer !== undefined &&
      (Array.isArray(userAnswer)
        ? userAnswer.length > 0
        : String(userAnswer).trim() !== "");
  }
}

class AssignmentHistoryDTO {
  constructor({
    attemptId,
    assignmentApplicationId,
    assignmentId,
    lessonId,
    title,
    subjectName,
    assignmentType,
    totalScore,
    score,
    percentage,
    answeredCount,
    correctCount,
    startedAt,
    submittedAt,
    questions,
  }) {
    this.attemptId = attemptId;
    this.assignmentApplicationId = assignmentApplicationId;
    this.assignmentId = assignmentId;
    this.lessonId = lessonId;
    this.title = title;
    this.subjectName = subjectName;
    this.assignmentType = assignmentType;
    this.totalScore = totalScore;
    this.score = score;
    this.percentage = percentage;
    this.answeredCount = answeredCount;
    this.correctCount = correctCount;
    this.startedAt = startedAt;
    this.submittedAt = submittedAt;
    this.questions = questions || [];
    this.questionCount = this.questions.length;
    this.wrongCount = Math.max(0, this.answeredCount - this.correctCount);
    this.unansweredCount = Math.max(0, this.questionCount - this.answeredCount);
  }
}

module.exports = {
  AssignmentHistoryDTO,
  AssignmentHistoryQuestionDTO,
  AssignmentHistoryOptionDTO,
};
