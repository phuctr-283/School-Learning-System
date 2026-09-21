(() => {
  "use strict";

  const QUESTION_TYPES = Object.freeze({
    MULTIPLE_CHOICE: "multiple_choice",
    ORDERING: "ordering",
    DRAG_AND_DROP: "drag_and_drop",
  });

  const initAssignmentBuilder = () => {
    const form = document.getElementById("assignment-form");

    const container = document.getElementById("questions");

    const addButton = document.getElementById("add-question");

    const emptyState = document.getElementById("question-empty");

    const questionsInput = document.getElementById("questions-json");

    if (!form || !container || !addButton || !emptyState || !questionsInput) {
      return;
    }

    if (form.dataset.initialized === "true") {
      return;
    }

    form.dataset.initialized = "true";

    const escapeHtml = (value = "") =>
      String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

    const normalizeLines = (value = "") =>
      String(value)
        .split(/\r?\n/)
        .map((line) => line.trim())
        .filter(Boolean);

    const countBlanks = (content = "") =>
      (String(content).match(/___/g) || []).length;

    const countMarkedAnswers = (lines = []) =>
      lines.filter((line) => line.startsWith("*")).length;

    const updateEmptyState = () => {
      emptyState.hidden = container.children.length > 0;
    };

    const updateQuestionNumbers = () => {
      [...container.children].forEach((editor, index) => {
        const element = editor.querySelector(".assignment-question__number");

        if (element) {
          element.textContent = `Câu ${index + 1}`;
        }
      });
    };

    const getQuestionData = (editor) => {
      return {
        question_type:
          editor.querySelector(".question-type")?.value?.trim() || "",

        question: editor.querySelector(".question")?.value?.trim() || "",

        content: editor.querySelector(".content")?.value || "",

        answer: editor.querySelector(".answer")?.value || "",

        score: editor.querySelector(".question-score")?.value?.trim() || "",
      };
    };

    const renderQuestionFields = (editor, type, data = {}) => {
      const target = editor.querySelector(".assignment-question__body");

      if (!target) {
        return;
      }

      const question = escapeHtml(data.question || "");

      const content = escapeHtml(data.content || "");

      const answer = escapeHtml(data.answer || "");

      if (type === QUESTION_TYPES.MULTIPLE_CHOICE) {
        target.innerHTML = `
          <div class="assignment-field assignment-field--full">
            <label>
              Nội dung câu hỏi
            </label>

            <textarea
              class="question"
              rows="4"
              required
              placeholder="Nhập nội dung câu hỏi trắc nghiệm..."
            >${question}</textarea>
          </div>

          <div class="assignment-field assignment-field--full">
            <label>
              Nội dung bổ sung
              <span class="assignment-field__hint">
                Không bắt buộc
              </span>
            </label>

            <textarea
              class="content"
              rows="3"
              placeholder="Có thể bỏ trống..."
            >${content}</textarea>
          </div>

          <div class="assignment-field assignment-field--full">
            <label>
              Đáp án
            </label>

            <textarea
              class="answer"
              rows="6"
              required
              placeholder="Hà Nội
*Sài Gòn
Huế"
            >${answer}</textarea>

            <small class="assignment-field__hint">
              Mỗi đáp án một dòng.
              Đáp án đúng bắt đầu bằng dấu
              <strong>*</strong>.
            </small>
          </div>
        `;

        return;
      }

      if (type === QUESTION_TYPES.ORDERING) {
        target.innerHTML = `
          <div class="assignment-field assignment-field--full">
            <label>
              Nội dung câu hỏi
            </label>

            <textarea
              class="question"
              rows="4"
              required
              placeholder="Hãy sắp xếp các bước sau..."
            >${question}</textarea>
          </div>

          <div class="assignment-field assignment-field--full">
            <label>
              Nội dung bổ sung
              <span class="assignment-field__hint">
                Không bắt buộc
              </span>
            </label>

            <textarea
              class="content"
              rows="3"
              placeholder="Có thể bỏ trống..."
            >${content}</textarea>
          </div>

          <div class="assignment-field assignment-field--full">
            <label>
              Đáp án theo thứ tự đúng
            </label>

            <textarea
              class="answer assignment-code-editor"
              rows="8"
              required
              spellcheck="false"
              placeholder="Bước 1
Bước 2
Bước 3"
            >${answer}</textarea>

            <small class="assignment-field__hint">
              Mỗi dòng là một đáp án theo thứ tự đúng.
              Không sử dụng dấu
              <strong>*</strong>.
            </small>
          </div>
        `;

        return;
      }

      if (type === QUESTION_TYPES.DRAG_AND_DROP) {
        target.innerHTML = `
          <div class="assignment-field assignment-field--full">
            <label>
              Nội dung câu hỏi
            </label>

            <textarea
              class="question"
              rows="4"
              required
              placeholder="Điền phần còn thiếu..."
            >${question}</textarea>
          </div>

          <div class="assignment-field assignment-field--full">
            <label>
              Nội dung có chỗ khuyết
            </label>

            <textarea
              class="content assignment-code-editor"
              rows="10"
              required
              spellcheck="false"
              placeholder="total = 0
___
return total"
            >${content}</textarea>

            <small class="assignment-field__hint">
              Nội dung phải có ít nhất một ký hiệu
              <strong>___</strong>.
            </small>
          </div>

          <div class="assignment-field assignment-field--full">
            <label>
              Đáp án
            </label>

            <textarea
              class="answer assignment-code-editor"
              rows="8"
              required
              spellcheck="false"
              placeholder="*for item in items:
*total += item
sai"
            >${answer}</textarea>

            <small class="assignment-field__hint">
              Số dòng bắt đầu bằng
              <strong>*</strong>
              phải bằng số ký hiệu
              <strong>___</strong>.
            </small>
          </div>
        `;
      }
    };

    const validateQuestion = (data, number) => {
      const type = data.question_type;

      const question = data.question.trim();

      const content = data.content.trim();

      const answerLines = normalizeLines(data.answer);

      if (!Object.values(QUESTION_TYPES).includes(type)) {
        throw new Error(`Câu ${number} có loại câu hỏi không hợp lệ.`);
      }

      if (!question) {
        throw new Error(`Câu ${number} chưa nhập nội dung câu hỏi.`);
      }

      if (answerLines.length === 0) {
        throw new Error(`Câu ${number} phải có ít nhất một đáp án.`);
      }

      const markedCount = countMarkedAnswers(answerLines);

      if (type === QUESTION_TYPES.MULTIPLE_CHOICE) {
        if (answerLines.length < 2) {
          throw new Error(`Câu ${number} phải có ít nhất 2 đáp án.`);
        }

        if (markedCount !== 1) {
          throw new Error(
            `Câu ${number} phải có đúng 1 đáp án bắt đầu bằng dấu *.`,
          );
        }
      }

      if (type === QUESTION_TYPES.ORDERING) {
        if (answerLines.length < 2) {
          throw new Error(`Câu ${number} phải có ít nhất 2 đáp án.`);
        }

        if (markedCount > 0) {
          throw new Error(
            `Câu ${number} dạng ordering không được sử dụng dấu *.`,
          );
        }
      }

      if (type === QUESTION_TYPES.DRAG_AND_DROP) {
        if (!content) {
          throw new Error(`Câu ${number} bắt buộc phải có content.`);
        }

        const blankCount = countBlanks(content);

        if (blankCount < 1) {
          throw new Error(`Câu ${number} phải có ít nhất một ký hiệu ___.`);
        }

        if (markedCount !== blankCount) {
          throw new Error(
            `Câu ${number} có ${blankCount} vị trí ___ nhưng có ${markedCount} đáp án đúng.`,
          );
        }
      }

      return {
        question_type: type,
        question,
        content,
        answer: answerLines.join("\n"),
      };
    };

    const collectQuestions = () => {
      return [...container.children].map((editor, index) => {
        const data = getQuestionData(editor);

        const result = validateQuestion(data, index + 1);

        if (data.score !== "") {
          const score = Number(data.score);

          if (!Number.isFinite(score) || score <= 0) {
            throw new Error(`Điểm câu ${index + 1} phải lớn hơn 0.`);
          }

          result.score = score;
        }

        return result;
      });
    };

    const addQuestion = (initialData = {}) => {
      const editor = document.createElement("section");

      editor.className = "assignment-question";

      editor.innerHTML = `
        <div class="assignment-question__top">
          <div class="assignment-question__title">
            <span class="assignment-question__number">
              Câu 1
            </span>

            <div>
              <strong>Câu hỏi</strong>
              <small>
                Chọn dạng câu hỏi và điểm số
              </small>
            </div>
          </div>

          <div class="assignment-question__tools">
            <select
              class="assignment-question__type question-type"
              required
            >
              <option value="multiple_choice">
                Trắc nghiệm
              </option>

              <option value="ordering">
                Sắp xếp thứ tự
              </option>

              <option value="drag_and_drop">
                Kéo thả điền khuyết
              </option>
            </select>

            <div class="assignment-question__score">
              <label>
                Điểm
              </label>

              <input
                class="question-score"
                type="number"
                min="0"
                step="0.25"
                inputmode="decimal"
                placeholder="Tùy chọn"
              />
            </div>

            <button
              type="button"
              class="assignment-question__remove"
            >
              <i class="fa-light fa-trash"></i>
              <span>Xóa</span>
            </button>
          </div>
        </div>

        <div class="assignment-question__body"></div>
      `;

      container.appendChild(editor);

      const typeSelector = editor.querySelector(".question-type");

      const scoreInput = editor.querySelector(".question-score");

      const removeButton = editor.querySelector(".assignment-question__remove");

      const initialType =
        initialData.question_type || QUESTION_TYPES.MULTIPLE_CHOICE;

      typeSelector.value = initialType;

      if (
        initialData.score !== undefined &&
        initialData.score !== null &&
        initialData.score !== ""
      ) {
        scoreInput.value = initialData.score;
      }

      renderQuestionFields(editor, initialType, initialData);

      typeSelector.addEventListener("change", () => {
        const oldData = getQuestionData(editor);

        renderQuestionFields(editor, typeSelector.value, oldData);

        scoreInput.value = oldData.score;
      });

      removeButton.addEventListener("click", () => {
        editor.remove();

        updateQuestionNumbers();
        updateEmptyState();
      });

      updateQuestionNumbers();
      updateEmptyState();
    };

    const validateAssignment = () => {
      const title =
        document.getElementById("assignment-title")?.value.trim() || "";

      const subject = form.querySelector(
        'input[name="subject_id"], select[name="subject_id"]',
      );

      const subjectId = subject?.value.trim() || "";

      const type =
        document.getElementById("assignment-type")?.value.trim() || "";

      const duration = Number(
        document.getElementById("assignment-duration")?.value,
      );

      if (!title) {
        throw new Error("Vui lòng nhập tên bài tập.");
      }

      if (!subjectId) {
        throw new Error("Vui lòng chọn môn học.");
      }

      if (!type) {
        throw new Error("Vui lòng chọn loại bài tập.");
      }

      if (!Number.isInteger(duration) || duration < 1 || duration > 600) {
        throw new Error("Thời gian làm bài phải từ 1 đến 600 phút.");
      }
    };

    addButton.addEventListener("click", () => addQuestion());

    form.addEventListener("submit", (event) => {
      event.preventDefault();

      try {
        validateAssignment();

        const questions = collectQuestions();

        if (questions.length === 0) {
          throw new Error("Vui lòng thêm ít nhất một câu hỏi.");
        }

        questionsInput.value = JSON.stringify(questions);

        HTMLFormElement.prototype.submit.call(form);
      } catch (error) {
        window.alert(error.message || "Dữ liệu bài tập không hợp lệ.");
      }
    });

    const initialQuestionsElement = document.getElementById(
      "initial-questions-data",
    );

    let initialQuestions = [];

    if (initialQuestionsElement) {
      try {
        initialQuestions = JSON.parse(
          initialQuestionsElement.textContent || "[]",
        );
      } catch {
        initialQuestions = [];
      }
    }

    initialQuestions.forEach((question) => {
      addQuestion(question);
    });

    if (initialQuestions.length === 0) {
      addQuestion();
    }

    updateQuestionNumbers();
    updateEmptyState();
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAssignmentBuilder, {
      once: true,
    });
  } else {
    initAssignmentBuilder();
  }
})();
