document.addEventListener("DOMContentLoaded", () => {
  initializeAssignment();
});

function initializeAssignment() {
  const page = document.querySelector(".exercise-page");

  if (!page) {
    return;
  }

  const form = document.getElementById("assignmentForm");

  const cards = Array.from(document.querySelectorAll(".question-card"));

  const savedAnswers = readSavedAnswers();

  let remainingSeconds = Number(page.dataset.remainingSeconds || 0);

  let attemptId = page.dataset.attemptId || "";

  let submitted = false;

  let saveTimer = null;

  let saveRequest = null;

  let timerInterval = null;

  initializeQuestionCards(cards, savedAnswers);

  initializeNavigation(cards);

  initializeMarkButtons(cards);

  initializeSubmit(page, form);

  initializeFullscreen();

  initializeBackButton(page);

  updateProgress(cards);

  startTimer();

  window.addEventListener("pagehide", saveBeforeLeave);

  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") {
      saveBeforeLeave();
    }
  });

  function startTimer() {
    renderTimer();

    timerInterval = setInterval(async () => {
      if (submitted) {
        return;
      }

      remainingSeconds -= 1;

      if (remainingSeconds <= 0) {
        remainingSeconds = 0;

        renderTimer();

        clearInterval(timerInterval);

        await handleTimeout();

        return;
      }

      renderTimer();
    }, 1000);
  }

  function renderTimer() {
    const timerText = document.getElementById("timerText");

    if (!timerText) {
      return;
    }

    const minutes = Math.floor(remainingSeconds / 60);

    const seconds = remainingSeconds % 60;

    timerText.textContent = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;

    const timer = document.getElementById("exerciseTimer");

    if (remainingSeconds <= 60) {
      timer?.classList.add("is-danger");
    }
  }

  async function handleTimeout() {
    if (submitted) {
      return;
    }

    const modal = document.getElementById("timeoutModal");

    if (modal) {
      modal.hidden = false;
    }

    try {
      await saveAnswers();

      await submitAssignment(true);
    } catch (error) {
      console.error("AUTO SUBMIT ERROR:", error);

      await submitAssignment(true);
    }
  }

  async function saveBeforeLeave() {
    if (submitted) {
      return;
    }

    const payload = JSON.stringify({
      attempt_id: attemptId,
      answers: collectAnswers(),
    });

    const saveUrl = page.dataset.saveUrl;

    if (!saveUrl) {
      return;
    }

    try {
      const blob = new Blob([payload], {
        type: "application/json",
      });

      navigator.sendBeacon(saveUrl, blob);
    } catch (error) {
      console.error("BEACON SAVE ERROR:", error);
    }
  }

  async function saveAnswers() {
    if (submitted) {
      return null;
    }

    const saveUrl = page.dataset.saveUrl;

    if (!saveUrl) {
      return null;
    }

    if (saveRequest) {
      try {
        await saveRequest;
      } catch (_) {
        // ignore
      }
    }

    const payload = {
      attempt_id: attemptId,

      answers: collectAnswers(),
    };

    saveRequest = fetch(saveUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then(async (response) => {
        const raw = await response.text();

        console.log("SAVE STATUS:", response.status);
        console.log("SAVE CONTENT-TYPE:", response.headers.get("content-type"));
        console.log("SAVE URL:", response.url);
        console.log("SAVE RESPONSE:", raw);

        let data = null;

        if (raw) {
          try {
            data = JSON.parse(raw);
          } catch (error) {
            console.error("SAVE RESPONSE KHÔNG PHẢI JSON:", raw);

            throw new Error(
              `API lưu bài trả về ${response.status} nhưng không phải JSON.`,
            );
          }
        }

        if (!response.ok) {
          throw new Error(
            data?.message ||
              data?.error ||
              `Không thể lưu bài. HTTP ${response.status}`,
          );
        }

        if (data?.data?.remaining_seconds !== undefined) {
          remainingSeconds = Number(data.data.remaining_seconds);

          renderTimer();
        }

        return data;
      })
      .finally(() => {
        saveRequest = null;
      });

    return saveRequest;
  }

  function scheduleSave() {
    clearTimeout(saveTimer);

    saveTimer = setTimeout(() => {
      saveAnswers().catch((error) => {
        console.error("AUTOSAVE ERROR:", error);
      });
    }, 700);
  }

  function initializeQuestionCards(cards, saved) {
    cards.forEach((card) => {
      const type = card.dataset.type;

      if (type === "multiple_choice") {
        initializeMultipleChoice(card, saved);
      }

      if (type === "drag_and_drop") {
        initializeDragAndDrop(card, saved);
      }

      if (type === "ordering") {
        initializeOrdering(card, saved);
      }
    });
  }

  function initializeMultipleChoice(card, saved) {
    const questionId = card.dataset.questionId;

    const radios = Array.from(card.querySelectorAll('input[type="radio"]'));

    const savedValue = normalizeSavedAnswer(saved[questionId]);

    if (typeof savedValue === "string") {
      const radio = radios.find((item) => item.value === savedValue);

      if (radio) {
        radio.checked = true;
      }
    }

    radios.forEach((radio) => {
      radio.addEventListener("change", () => {
        updateProgress(cards);

        scheduleSave();
      });
    });
  }

  function initializeDragAndDrop(card, saved) {
    const template = card.querySelector("[data-template-source]");

    const options = Array.from(card.querySelectorAll(".drag-option"));

    if (!template) {
      return;
    }

    const rawTemplate = template.textContent || "";

    renderTemplateWithGaps(template, rawTemplate);

    const gaps = Array.from(template.querySelectorAll(".blank-gap"));

    options.forEach((option) => {
      option.addEventListener("click", () => {
        const gap = gaps.find((item) => !item.dataset.optionId);

        if (!gap) {
          return;
        }

        setGapValue(gap, option);

        updateDragState(card);

        updateProgress(cards);

        scheduleSave();
      });
    });

    gaps.forEach((gap) => {
      gap.addEventListener("click", () => {
        clearGapValue(gap, card);

        updateDragState(card);

        updateProgress(cards);

        scheduleSave();
      });
    });

    restoreDragAnswer(card, saved[card.dataset.questionId]);
  }

  function renderTemplateWithGaps(container, template) {
    container.innerHTML = "";

    const parts = template.split(/_{3,}/);

    parts.forEach((part, index) => {
      container.appendChild(document.createTextNode(part));

      if (index < parts.length - 1) {
        const gap = document.createElement("button");

        gap.type = "button";

        gap.className = "blank-gap";

        gap.dataset.gapIndex = String(index);

        gap.innerHTML = `
            <span class="blank-gap__placeholder">
              Chọn đáp án
            </span>
          `;

        container.appendChild(gap);
      }
    });
  }

  function setGapValue(gap, option) {
    gap.dataset.optionId = option.dataset.optionId;

    gap.classList.add("is-filled");

    gap.innerHTML = `
      <span class="blank-gap__value">
        ${escapeHtml(
          option.querySelector(".drag-option__text")?.textContent ||
            option.textContent,
        )}
      </span>
    `;

    option.classList.add("is-used");
  }

  function clearGapValue(gap, card) {
    const optionId = gap.dataset.optionId;

    if (!optionId) {
      return;
    }

    const option = card.querySelector(
      `.drag-option[data-option-id="${cssEscape(optionId)}"]`,
    );

    if (option) {
      option.classList.remove("is-used");
    }

    delete gap.dataset.optionId;

    gap.classList.remove("is-filled");

    gap.innerHTML = `
      <span class="blank-gap__placeholder">
        Chọn đáp án
      </span>
    `;
  }

  function updateDragState(card) {
    // Chỉ dùng để trigger state update.
    // Answer thực tế luôn được lấy trực tiếp
    // từ các blank khi save.
  }

  function restoreDragAnswer(card, rawAnswer) {
    const answer = normalizeSavedAnswer(rawAnswer);

    if (!Array.isArray(answer)) {
      return;
    }

    const gaps = Array.from(card.querySelectorAll(".blank-gap"));

    answer.forEach((optionId, index) => {
      if (optionId === null || optionId === undefined) {
        return;
      }

      const gap = gaps[index];

      if (!gap) {
        return;
      }

      const option = card.querySelector(
        `.drag-option[data-option-id="${cssEscape(String(optionId))}"]`,
      );

      if (!option) {
        return;
      }

      setGapValue(gap, option);
    });
  }

  function initializeOrdering(card, saved) {
    const source = card.querySelector("[data-ordering-source]");

    const answer = card.querySelector("[data-ordering-answer]");

    if (!source || !answer) {
      return;
    }

    const shouldShuffle = card.dataset.shuffleOptions === "true";

    if (shouldShuffle) {
      shuffleChildren(source);
    }

    Array.from(source.querySelectorAll(".ordering-item")).forEach((item) => {
      item.addEventListener("click", () => {
        answer.appendChild(item);

        answer.classList.add("has-items");

        updateOrderingNumbers(card);

        updateProgress(cards);

        scheduleSave();
      });
    });

    // Event delegation
    answer.addEventListener("click", (event) => {
      const item = event.target.closest(".ordering-item");

      if (!item) {
        return;
      }

      source.appendChild(item);

      updateOrderingNumbers(card);

      updateProgress(cards);

      scheduleSave();
    });

    restoreOrderingAnswer(card, saved[card.dataset.questionId]);
  }

  function restoreOrderingAnswer(card, rawAnswer) {
    const answer = normalizeSavedAnswer(rawAnswer);

    if (!Array.isArray(answer)) {
      return;
    }

    const source = card.querySelector("[data-ordering-source]");

    const target = card.querySelector("[data-ordering-answer]");

    if (!source || !target) {
      return;
    }

    answer.forEach((optionId) => {
      if (optionId === null || optionId === undefined) {
        return;
      }

      const item = source.querySelector(
        `.ordering-item[data-option-id="${cssEscape(String(optionId))}"]`,
      );

      if (item) {
        target.appendChild(item);
      }
    });

    updateOrderingNumbers(card);
  }

  function updateOrderingNumbers(card) {
    const answer = card.querySelector("[data-ordering-answer]");

    if (!answer) {
      return;
    }

    const items = Array.from(answer.querySelectorAll(".ordering-item"));

    answer.classList.toggle("has-items", items.length > 0);

    items.forEach((item, index) => {
      const number = item.querySelector(".ordering-item__number");

      if (number) {
        number.textContent = String(index + 1);
      }
    });
  }

  function collectAnswers() {
    const result = {};

    cards.forEach((card) => {
      const questionId = card.dataset.questionId;

      const type = card.dataset.type;

      if (type === "multiple_choice") {
        const selected = card.querySelector('input[type="radio"]:checked');

        result[questionId] = selected ? selected.value : null;
      }

      if (type === "drag_and_drop") {
        const gaps = Array.from(card.querySelectorAll(".blank-gap"));

        result[questionId] = gaps.map((gap) => gap.dataset.optionId || null);
      }

      if (type === "ordering") {
        const items = Array.from(
          card.querySelectorAll("[data-ordering-answer] .ordering-item"),
        );

        result[questionId] = items.map((item) => item.dataset.optionId);
      }
    });

    return result;
  }

  function initializeNavigation(cards) {
    const navigation = document.getElementById("questionNavigation");

    if (!navigation) {
      return;
    }

    const buttons = Array.from(
      navigation.querySelectorAll(".question-nav-item"),
    );

    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        const index = Number(button.dataset.index);

        cards[index]?.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      });
    });
  }

  function updateProgress(cards) {
    let answered = 0;

    cards.forEach((card) => {
      const type = card.dataset.type;

      let isAnswered = false;

      if (type === "multiple_choice") {
        isAnswered = Boolean(card.querySelector('input[type="radio"]:checked'));
      }

      if (type === "drag_and_drop") {
        const gaps = Array.from(card.querySelectorAll(".blank-gap"));

        isAnswered =
          gaps.length > 0 && gaps.every((gap) => Boolean(gap.dataset.optionId));
      }

      if (type === "ordering") {
        const items = card.querySelectorAll(
          "[data-ordering-answer] .ordering-item",
        );

        const source = card.querySelector("[data-ordering-source]");

        isAnswered =
          items.length > 0 &&
          source &&
          source.querySelectorAll(".ordering-item").length === 0;
      }

      card.classList.toggle("is-answered", isAnswered);

      const nav = document.querySelector(
        `.question-nav-item[data-index="${card.dataset.index}"]`,
      );

      nav?.classList.toggle("is-answered", isAnswered);

      if (isAnswered) {
        answered += 1;
      }
    });

    const total = cards.length;

    const progressText = document.getElementById("progressText");

    if (progressText) {
      progressText.textContent = `${answered}/${total}`;
    }

    const progressBar = document.getElementById("progressBar");

    if (progressBar) {
      const percent = total === 0 ? 0 : (answered / total) * 100;

      progressBar.style.width = `${percent}%`;
    }
  }

  function initializeMarkButtons(cards) {
    cards.forEach((card) => {
      const button = card.querySelector("[data-mark-question]");

      if (!button) {
        return;
      }

      button.addEventListener("click", () => {
        button.classList.toggle("is-marked");

        const icon = button.querySelector("i");

        if (button.classList.contains("is-marked")) {
          icon?.classList.remove("fa-light");

          icon?.classList.add("fa-solid");
        } else {
          icon?.classList.remove("fa-solid");

          icon?.classList.add("fa-light");
        }
      });
    });
  }

  function initializeSubmit(page, form) {
    const submitButton = document.getElementById("btnSubmit");
    const confirmButton = document.getElementById("btnConfirmSubmit");
    const modal = document.getElementById("confirmModal");

    if (!submitButton) {
      console.error("Không tìm thấy #btnSubmit");
      return;
    }

    if (!modal) {
      console.error("Không tìm thấy #confirmModal");
      return;
    }

    submitButton.addEventListener("click", (event) => {
      event.preventDefault();
      console.log("CLICK NỘP BÀI");

      if (submitted) {
        console.log("Đã submitted");
        return;
      }

      modal.hidden = false;
    });

    document.querySelectorAll("[data-close-modal]").forEach((button) => {
      button.addEventListener("click", (event) => {
        event.preventDefault();

        const currentModal = button.closest(".exercise-modal");

        if (currentModal) {
          currentModal.hidden = true;
        }
      });
    });

    const overlay = modal.querySelector(".exercise-modal__overlay");

    overlay?.addEventListener("click", () => {
      modal.hidden = true;
    });

    if (confirmButton) {
      confirmButton.addEventListener("click", async (event) => {
        event.preventDefault();

        if (submitted) {
          return;
        }

        modal.hidden = true;

        await submitAssignment(false);
      });
    }

    document.querySelector("#btnResultBack")?.addEventListener("click", () => {
      window.location.href = page.dataset.backUrl || "/";
    });
  }

  async function submitAssignment(automatic) {
    if (submitted) {
      return;
    }

    if (automatic) {
      const timeoutModal = document.getElementById("timeoutModal");

      if (timeoutModal) {
        timeoutModal.hidden = false;
      }
    }

    if (timerInterval) {
      clearInterval(timerInterval);
    }

    clearTimeout(saveTimer);

    const submitUrl = page.dataset.submitUrl;

    if (!submitUrl) {
      console.error("Không có submit URL.");
      return;
    }

    const answers = collectAnswers();

    const payload = {
      attempt_id: attemptId,
      answers: answers,
    };

    console.log("SUBMIT URL:", submitUrl);
    console.log("SUBMIT PAYLOAD:", payload);
    console.log("SUBMIT JSON:", JSON.stringify(payload));

    const button = document.getElementById("btnSubmit");

    if (button) {
      button.disabled = true;

      button.innerHTML = `
      <i class="fa-light fa-spinner fa-spin"></i>
      Đang nộp...
    `;
    }

    try {
      const response = await fetch(submitUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify(payload),
      });

      const raw = await response.text();

      console.log("SUBMIT STATUS:", response.status);
      console.log("SUBMIT CONTENT-TYPE:", response.headers.get("content-type"));
      console.log("SUBMIT URL:", response.url);
      console.log("SUBMIT RAW RESPONSE:", raw);

      let data = null;

      if (raw) {
        try {
          data = JSON.parse(raw);
        } catch (parseError) {
          console.error("SUBMIT RESPONSE KHÔNG PHẢI JSON:", raw);

          throw new Error(
            `API nộp bài trả về ${response.status} nhưng không phải JSON.`,
          );
        }
      }

      if (!response.ok) {
        throw new Error(
          data?.message ||
            data?.error ||
            `Không thể nộp bài. HTTP ${response.status}`,
        );
      }

      if (!data) {
        throw new Error("Server không trả về dữ liệu.");
      }

      if (!response.ok) {
        throw new Error(data?.message || data?.error || "Không thể nộp bài.");
      }

      if (!data) {
        throw new Error("Server không trả về dữ liệu.");
      }

      submitted = true;

      renderResult(data.data);
    } catch (error) {
      console.error("SUBMIT ERROR:", error);

      submitted = false;

      if (button) {
        button.disabled = false;

        button.innerHTML = `
        <i class="fa-light fa-paper-plane"></i>
        Nộp bài
      `;
      }

      const timeoutModal = document.getElementById("timeoutModal");

      if (timeoutModal) {
        timeoutModal.hidden = true;
      }

      alert(error.message || "Không thể nộp bài.");
    }
  }

  function renderResult(result) {
    const resultBox = document.getElementById("exerciseResult");

    const questionList = document.querySelector(".question-list");

    const submitBar = document.querySelector(".exercise-submit-bar");

    if (questionList) {
      questionList.hidden = true;
    }

    if (submitBar) {
      submitBar.hidden = true;
    }

    if (resultBox) {
      resultBox.hidden = false;
    }

    const score = document.getElementById("resultScore");

    if (score) {
      score.textContent = `${result.score} / ${result.total_score} điểm (${result.percentage}%)`;
    }

    const review = document.getElementById("resultReview");

    if (!review) {
      return;
    }

    review.innerHTML = "";

    (result.review || []).forEach((item, index) => {
      const element = document.createElement("div");

      element.className =
        "result-review__item " + (item.correct ? "is-correct" : "is-wrong");

      element.innerHTML = `
          <strong>
            Câu ${index + 1}:
            ${item.correct ? "Đúng" : "Sai"}
          </strong>
          `;

      review.appendChild(element);
    });
  }

  function initializeFullscreen() {
    const button = document.getElementById("btnFullscreen");

    if (!button) {
      return;
    }

    button.addEventListener("click", async () => {
      try {
        if (!document.fullscreenElement) {
          await document.documentElement.requestFullscreen();
        } else {
          await document.exitFullscreen();
        }
      } catch (error) {
        console.error("FULLSCREEN ERROR:", error);
      }
    });
  }

  function initializeBackButton(page) {
    document.getElementById("btnBack")?.addEventListener("click", async () => {
      if (submitted) {
        window.location.href = page.dataset.backUrl || "/";

        return;
      }

      await saveAnswers();

      window.location.href = page.dataset.backUrl || "/";
    });
  }

  function readSavedAnswers() {
    const element = document.getElementById("saved-answers-data");

    if (!element) {
      return {};
    }

    try {
      const raw = element.value || element.textContent || "{}";

      return JSON.parse(raw);
    } catch (error) {
      console.error("SAVED ANSWERS PARSE ERROR:", error);

      return {};
    }
  }

  function normalizeSavedAnswer(value) {
    if (typeof value !== "string") {
      return value;
    }

    try {
      return JSON.parse(value);
    } catch (_) {
      return value;
    }
  }

  function shuffleChildren(container) {
    const children = Array.from(container.children);

    for (let i = children.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));

      [children[i], children[j]] = [children[j], children[i]];
    }

    children.forEach((child) => container.appendChild(child));
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function cssEscape(value) {
    if (window.CSS && typeof CSS.escape === "function") {
      return CSS.escape(value);
    }

    return String(value).replace(/["\\]/g, "\\$&");
  }
}
