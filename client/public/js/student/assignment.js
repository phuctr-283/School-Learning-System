document.addEventListener("DOMContentLoaded", () => {
  initializeAssignment();
});

function initializeAssignment() {
  const page = document.querySelector(".exercise-page");

  if (!page || page.dataset.initialized === "true") {
    return;
  }

  page.dataset.initialized = "true";

  const cards = Array.from(page.querySelectorAll(".question-card"));

  const savedAnswers = readSavedAnswers();

  let remainingSeconds = Math.max(
    0,
    Number(page.dataset.remainingSeconds || 0),
  );

  const attemptId = page.dataset.attemptId || "";

  let submitted = false;
  let saveTimer = null;
  let saveRequest = null;
  let timerInterval = null;

  initializeQuestionCards(cards, savedAnswers);
  initializeNavigation(cards);
  initializeMarkButtons(cards);
  initializeCurrentQuestion(cards);
  initializeSubmit();
  initializeFullscreen();

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

    if (remainingSeconds <= 0) {
      handleTimeout();
      return;
    }

    timerInterval = setInterval(async () => {
      if (submitted) {
        return;
      }

      remainingSeconds = Math.max(0, remainingSeconds - 1);

      renderTimer();

      if (remainingSeconds === 0) {
        clearInterval(timerInterval);

        await handleTimeout();
      }
    }, 1000);
  }
  function normalizeDisplayText(value) {
    return String(value ?? "").replace(/^\s+/, "");
  }
  function renderTimer() {
    const timerText = page.querySelector("#timerText");
    const timer = page.querySelector("#exerciseTimer");

    if (!timerText) {
      return;
    }

    const minutes = Math.floor(remainingSeconds / 60);

    const seconds = remainingSeconds % 60;

    timerText.textContent =
      `${String(minutes).padStart(2, "0")}:` +
      `${String(seconds).padStart(2, "0")}`;

    timer?.classList.toggle(
      "is-warning",
      remainingSeconds <= 300 && remainingSeconds > 60,
    );

    timer?.classList.toggle("is-danger", remainingSeconds <= 60);
  }

  function setSaveStatus(type, text) {
    const status = page.querySelector("#saveStatus");

    if (!status) {
      return;
    }

    status.className = `exercise-save-status is-${type}`;

    const icon =
      type === "saving"
        ? "fa-spinner fa-spin"
        : type === "error"
          ? "fa-cloud-xmark"
          : "fa-cloud-check";

    status.innerHTML = `
      <i class="fa-light ${icon}"></i>
      <span>${text}</span>
    `;
  }

  async function handleTimeout() {
    if (submitted) {
      return;
    }

    const modal = page.querySelector("#timeoutModal");

    if (modal) {
      modal.hidden = false;
    }

    try {
      await saveAnswers();
    } catch (error) {
      console.error("TIMEOUT SAVE ERROR:", error);
    }

    await submitAssignment(true);
  }

  function saveBeforeLeave() {
    if (submitted) {
      return;
    }

    const saveUrl = page.dataset.saveUrl;

    if (!saveUrl) {
      return;
    }

    try {
      const payload = JSON.stringify({
        attempt_id: attemptId,
        answers: collectAnswers(),
      });

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
      } catch (_) {}
    }

    setSaveStatus("saving", "Đang lưu...");

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

        let data = null;

        if (raw) {
          try {
            data = JSON.parse(raw);
          } catch (_) {
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

        const remaining = data?.data?.remaining_seconds;

        if (remaining !== undefined && remaining !== null) {
          remainingSeconds = Math.max(0, Number(remaining));

          renderTimer();
        }

        setSaveStatus("saved", "Đã lưu");

        return data;
      })
      .catch((error) => {
        setSaveStatus("error", "Lưu thất bại");

        throw error;
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

    const rawTemplate = normalizeDisplayText(template.textContent);
    renderTemplateWithGaps(template, rawTemplate);

    const gaps = Array.from(template.querySelectorAll(".blank-gap"));

    options.forEach((option) => {
      option.addEventListener("click", () => {
        if (option.classList.contains("is-used")) {
          return;
        }

        const gap = gaps.find((item) => !item.dataset.optionId);

        if (!gap) {
          return;
        }

        setGapValue(gap, option);

        updateProgress(cards);

        scheduleSave();
      });
    });

    gaps.forEach((gap) => {
      gap.addEventListener("click", () => {
        clearGapValue(gap, card);

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

    option?.classList.remove("is-used");

    delete gap.dataset.optionId;

    gap.classList.remove("is-filled");

    gap.innerHTML = `
      <span class="blank-gap__placeholder">
        Chọn đáp án
      </span>
    `;
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

    source.addEventListener("click", (event) => {
      const item = event.target.closest(".ordering-item");

      if (!item || !source.contains(item)) {
        return;
      }

      answer.appendChild(item);

      updateOrderingNumbers(card);

      updateProgress(cards);

      scheduleSave();
    });

    answer.addEventListener("click", (event) => {
      const item = event.target.closest(".ordering-item");

      if (!item || !answer.contains(item)) {
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

    const empty = answer.querySelector(".ordering-empty");

    answer.classList.toggle("has-items", items.length > 0);

    if (empty) {
      empty.hidden = items.length > 0;
    }

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
    const navigation = page.querySelector("#questionNavigation");

    if (!navigation) {
      return;
    }

    navigation.querySelectorAll(".question-nav-item").forEach((button) => {
      button.addEventListener("click", () => {
        const index = Number(button.dataset.index);

        const card = cards[index];

        if (!card) {
          return;
        }

        card.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      });
    });
  }

  function initializeCurrentQuestion(cards) {
    if (!("IntersectionObserver" in window)) {
      cards[0]?.classList.add("is-current");

      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio);

        const card = visible[0]?.target;

        if (!card) {
          return;
        }

        cards.forEach((item) => {
          item.classList.toggle("is-current", item === card);
        });

        const nav = page.querySelector(
          `.question-nav-item[data-index="${card.dataset.index}"]`,
        );

        page.querySelectorAll(".question-nav-item").forEach((item) => {
          item.classList.toggle("is-current", item === nav);
        });
      },
      {
        threshold: [0.25, 0.5, 0.75],
        rootMargin: "-90px 0px -30% 0px",
      },
    );

    cards.forEach((card) => observer.observe(card));
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

      const nav = page.querySelector(
        `.question-nav-item[data-index="${card.dataset.index}"]`,
      );

      nav?.classList.toggle("is-answered", isAnswered);

      if (isAnswered) {
        answered += 1;
      }
    });

    const total = cards.length;

    const progressText = page.querySelector("#progressText");

    if (progressText) {
      progressText.textContent = `${answered}/${total}`;
    }

    const progressBar = page.querySelector("#progressBar");

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
        const marked = button.classList.toggle("is-marked");

        button.setAttribute("aria-pressed", String(marked));

        const icon = button.querySelector("i");

        icon?.classList.toggle("fa-light", !marked);

        icon?.classList.toggle("fa-solid", marked);
      });
    });
  }

  function initializeSubmit() {
    const submitButton = page.querySelector("#btnSubmit");

    const confirmButton = page.querySelector("#btnConfirmSubmit");

    const modal = page.querySelector("#confirmModal");

    if (!submitButton || !modal) {
      return;
    }

    submitButton.addEventListener("click", (event) => {
      event.preventDefault();

      if (submitted) {
        return;
      }

      modal.hidden = false;
    });

    page.querySelectorAll("[data-close-modal]").forEach((button) => {
      button.addEventListener("click", (event) => {
        event.preventDefault();

        button.closest(".exercise-modal").hidden = true;
      });
    });

    modal
      .querySelector(".exercise-modal__overlay")
      ?.addEventListener("click", () => {
        modal.hidden = true;
      });

    confirmButton?.addEventListener("click", async (event) => {
      event.preventDefault();

      if (submitted) {
        return;
      }

      modal.hidden = true;

      await submitAssignment(false);
    });

    page.querySelector("#btnResultBack")?.addEventListener("click", () => {
      window.location.href = "/student/assignment/qr";
    });
  }

  async function submitAssignment(automatic) {
    if (submitted) {
      return;
    }

    if (automatic) {
      const timeoutModal = page.querySelector("#timeoutModal");

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
      return;
    }

    const payload = {
      attempt_id: attemptId,
      answers: collectAnswers(),
    };

    const button = page.querySelector("#btnSubmit");

    if (button) {
      button.disabled = true;

      button.innerHTML = `
        <i class="fa-light fa-spinner fa-spin"></i>
        <span>Đang nộp...</span>
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

      let data = null;

      if (raw) {
        try {
          data = JSON.parse(raw);
        } catch (_) {
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

      submitted = true;

      page.querySelector("#timeoutModal")?.setAttribute("hidden", "");

      renderResult(data.data);
    } catch (error) {
      console.error("SUBMIT ERROR:", error);

      submitted = false;

      if (button) {
        button.disabled = false;

        button.innerHTML = `
          <i class="fa-light fa-paper-plane"></i>
          <span>Nộp bài</span>
        `;
      }

      page.querySelector("#timeoutModal")?.setAttribute("hidden", "");

      alert(error.message || "Không thể nộp bài.");
    }
  }

  function renderResult(result) {
  const resultBox = page.querySelector("#exerciseResult");

  if (!resultBox) {
    return;
  }

  resultBox.removeAttribute("hidden");
  resultBox.classList.add("is-visible");

  const score = page.querySelector("#resultScore");

  if (score) {
    const current = result?.score ?? 0;
    const total = result?.total_score ?? 0;
    const percentage = result?.percentage ?? 0;

    score.textContent =
      `${current} / ${total} điểm (${percentage}%)`;
  }
}
  function initializeFullscreen() {
    const button = page.querySelector("#btnFullscreen");

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

    document.addEventListener("fullscreenchange", () => {
      const icon = button.querySelector("i");

      if (!icon) {
        return;
      }

      const fullscreen = Boolean(document.fullscreenElement);

      icon.classList.toggle("fa-expand", !fullscreen);

      icon.classList.toggle("fa-compress", fullscreen);
    });
  }

  

  function readSavedAnswers() {
    const element = page.querySelector("#saved-answers-data");

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
