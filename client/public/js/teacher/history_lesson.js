console.log("LESSON OPENING JS LOADED");

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initializeLessonOpenings);
} else {
  initializeLessonOpenings();
}

function initializeLessonOpenings() {
  const container = document.querySelector(".lesson-opening-list");

  if (!container) {
    return;
  }

  const classSectionId = container.dataset.classSectionId;

  if (!classSectionId) {
    console.error("Không tìm thấy classSectionId.");

    return;
  }

  initializeContentToggles(container, classSectionId);
}

function initializeContentToggles(container, classSectionId) {
  container.addEventListener("click", async (event) => {
    const button = event.target.closest(".lesson-opening-content-toggle");

    if (!button) {
      return;
    }

    const lessonId = button.dataset.lessonId;

    const panelId = button.getAttribute("aria-controls");

    const panel = document.getElementById(panelId);

    if (!lessonId || !panel) {
      console.error("Không tìm thấy lessonId hoặc panel.", {
        lessonId,
        panelId,
      });

      return;
    }

    const isOpen = button.getAttribute("aria-expanded") === "true";

    if (isOpen) {
      panel.hidden = true;

      button.setAttribute("aria-expanded", "false");

      updateContentToggleIcon(button, false);

      return;
    }

    panel.hidden = false;

    button.setAttribute("aria-expanded", "true");

    updateContentToggleIcon(button, true);

    await loadLessonAssignments(panel, classSectionId, lessonId);
  });
}

function updateContentToggleIcon(button, isOpen) {
  const icon = button.querySelector(".lesson-opening-content-icon i");

  if (!icon) {
    return;
  }

  icon.className = `fa-light ${
    isOpen ? "fa-chevron-down" : "fa-chevron-right"
  }`;
}

async function loadLessonAssignments(panel, classSectionId, lessonId) {
  const assignmentContainer = panel.querySelector(".lesson-assignments");

  if (!assignmentContainer) {
    return;
  }

  const loading = assignmentContainer.querySelector(".assignment-loading");

  const list = assignmentContainer.querySelector(".assignment-list");

  const empty = assignmentContainer.querySelector(".assignment-empty");

  const error = assignmentContainer.querySelector(".assignment-error");

  loading.hidden = false;
  list.innerHTML = "";
  empty.hidden = true;
  error.hidden = true;

  try {
    const url =
      `/teacher/assignment/lesson-opening/applications` +
      `?class_section_id=${encodeURIComponent(classSectionId)}` +
      `&lesson_id=${encodeURIComponent(lessonId)}`;

    const response = await fetch(url, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      credentials: "same-origin",
    });

    const contentType = response.headers.get("content-type");

    const responseText = await response.text();

    if (!contentType || !contentType.includes("application/json")) {
      throw new Error(
        `Server không trả JSON. HTTP ${response.status}: ${responseText}`,
      );
    }

    const result = JSON.parse(responseText);

    if (!response.ok || result.success !== true) {
      throw new Error(result.message || "Không thể tải bài tập.");
    }

    const assignments = Array.isArray(result.data) ? result.data : [];

    if (assignments.length === 0) {
      empty.hidden = false;
      return;
    }

    renderAssignments(list, assignments, classSectionId);
  } catch (errorObject) {
    console.error("LOAD LESSON ASSIGNMENTS ERROR:", errorObject);

    error.textContent =
      errorObject.message || "Không thể tải danh sách bài tập.";

    error.hidden = false;
  } finally {
    loading.hidden = true;
  }
}

function renderAssignments(container, assignments, classSectionId) {
  container.innerHTML = assignments
    .map((assignment) => createAssignmentHTML(assignment, classSectionId))
    .join("");
}

function createAssignmentHTML(assignment, classSectionId) {
  const applicationId =
    assignment.assignment_application_id ??
    assignment.assignmentApplicationId ??
    "";

  const lessonId = assignment.lesson_id ?? assignment.lessonId ?? "";

  const title = assignment.title ?? "";

  const assignmentId =
    assignment.assignment_id ?? assignment.assignmentId ?? "";

  return `
    <a
      href="/teacher/assignment/applications/${encodeURIComponent(
        applicationId,
      )}/class-sections/${encodeURIComponent(
        classSectionId,
      )}/lessons/${encodeURIComponent(lessonId)}"
      class="lesson-assignment-item"
      data-assignment-application-id="${escapeHtml(applicationId)}"
      data-class-section-id="${escapeHtml(classSectionId)}"
      data-lesson-id="${escapeHtml(lessonId)}"
      data-assignment-id="${escapeHtml(assignmentId)}"
    >
      <div class="lesson-assignment-main">
        <div class="lesson-assignment-title">

          <span class="lesson-assignment-icon">
            <i class="fa-light fa-file-lines"></i>
          </span>

          <span class="lesson-assignment-title-text">
            ${escapeHtml(title)}
          </span>

        </div>
      </div>

      <span
        class="lesson-assignment-arrow"
        aria-hidden="true"
      >
        <i class="fa-light fa-chevron-right"></i>
      </span>
    </a>
  `;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
