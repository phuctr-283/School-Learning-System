const StudentAssignmentRepository = require("../../../domain/repositories/assignment/student_assignment_repository");

const assignmentStudentApi = require("../../api/assignment/assignment_student_api");
const errorApi = require("../../api/error_api");

const {
  AssignmentHistoryDTO,
  AssignmentHistoryQuestionDTO,
  AssignmentHistoryOptionDTO,
} = require("../../../application/assignments/dto/assignment_history.dto");
class StudentAssignmentRepositoryImpl extends StudentAssignmentRepository {
  async getStudentAssignment(params) {
    try {
      const response = await assignmentStudentApi.getStudentAssignment(params);

      if (!response?.success) {
        throw new errorApi(
          response?.message || "Không thể tải bài tập.",
          400,
          response,
        );
      }

      return response.data;
    } catch (error) {
      if (error instanceof errorApi) {
        throw error;
      }

      const status = error.response?.status || 500;

      const message =
        error.response?.data?.message ||
        error.message ||
        "Không thể tải bài tập.";

      throw new errorApi(message, status, error.response?.data);
    }
  }

  async saveAnswers(data) {
    try {
      const response = await assignmentStudentApi.saveAnswers(data);
      if (!response?.success) {
        throw new errorApi(
          response?.message || "Không thể lưu bài.",
          400,
          response,
        );
      }
      return response.data;
    } catch (error) {
      if (error instanceof errorApi) {
        throw error;
      }

      throw new errorApi(
        error.response?.data?.message || error.message || "Không thể lưu bài.",
        error.response?.status || 500,
        error.response?.data,
      );
    }
  }

  async submitAssignment(data) {
    try {
      const response = await assignmentStudentApi.submitAssignment(data);
      if (!response?.success) {
        throw new errorApi(
          response?.message || "Không thể nộp bài.",
          400,
          response,
        );
      }

      return response.data;
    } catch (error) {
      if (error instanceof errorApi) {
        throw error;
      }

      throw new errorApi(
        error.response?.data?.message || error.message || "Không thể nộp bài.",
        error.response?.status || 500,
        error.response?.data,
      );
    }
  }
  async getAssignmentHistory(
    req,
    assignmentApplicationId,
    classSectionId,
    studentId,
  ) {
    const response = await assignmentStudentApi.getAssignmentHistory(
      req,
      assignmentApplicationId,
      classSectionId,
      studentId,
    );
    const body = response?.data;
    if (!body) {
      throw new Error("Không có dữ liệu lịch sử bài làm.");
    }
    if (body.success === false) {
      throw new Error(body.message || "Không thể tải lịch sử bài làm.");
    }
    const data = body.data;
    if (!data) {
      throw new Error("Không có dữ liệu lịch sử bài làm.");
    }
    return new AssignmentHistoryDTO({
      attemptId: data.attempt_id,
      assignmentApplicationId: data.assignment_application_id,
      assignmentId: data.assignment_id,
      lessonId: data.lesson_id,
      title: data.title,
      subjectName: data.subject_name,
      assignmentType: data.assignment_type,
      totalScore: data.total_score,
      score: data.score,
      percentage: data.percentage,
      answeredCount: data.answered_count,
      correctCount: data.correct_count,
      startedAt: data.started_at,
      submittedAt: data.submitted_at,
      questions: (data.questions || []).map(
        (question) =>
          new AssignmentHistoryQuestionDTO({
            questionId: question.question_id,
            question: question.question,
            content: question.content,
            questionType: question.question_type,
            score: question.score,
            earnedScore: question.earned_score,
            userAnswer: question.user_answer,
            correctAnswer: question.correct_answer,
            correct: question.correct,
            options: (question.options || []).map(
              (option) =>
                new AssignmentHistoryOptionDTO({
                  optionId: option.option_id,
                  content: option.content,
                  isCorrect: option.is_correct,
                  isSelected: option.is_selected,
                  isSelectedCorrect: option.is_selected_correct,
                  isSelectedWrong: option.is_selected_wrong,
                }),
            ),
            correctOptions: (question.correct_options || []).map(
              (option) =>
                new AssignmentHistoryOptionDTO({
                  optionId: option.option_id,
                  content: option.content,
                  isCorrect: option.is_correct,
                  isSelected: option.is_selected,
                  isSelectedCorrect: option.is_selected_correct,
                  isSelectedWrong: option.is_selected_wrong,
                }),
            ),
            wrongOptions: (question.wrong_options || []).map(
              (option) =>
                new AssignmentHistoryOptionDTO({
                  optionId: option.option_id,
                  content: option.content,
                  isCorrect: option.is_correct,
                  isSelected: option.is_selected,
                  isSelectedCorrect: option.is_selected_correct,
                  isSelectedWrong: option.is_selected_wrong,
                }),
            ),
          }),
      ),
    });
  }
}

module.exports = StudentAssignmentRepositoryImpl;
