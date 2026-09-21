document.addEventListener("DOMContentLoaded", () => {
  initializeLessonOpenings();
});

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
  const buttons = container.querySelectorAll(".lesson-opening-content-toggle");

  buttons.forEach((button) => {
    button.addEventListener("click", async () => {
      const lessonId = button.dataset.lessonId;

      const panelId = button.getAttribute("aria-controls");

      const panel = document.getElementById(panelId);

      if (!lessonId || !panel) {
        console.error("Không tìm thấy lessonId hoặc panel.", {
          lessonId,
          panelId,
          panel,
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
  });
}

function updateContentToggleIcon(button, isOpen) {
  const icon = button.querySelector(".lesson-opening-content-icon i");

  if (!icon) {
    return;
  }

  icon.className = `fa-light ${isOpen ? "fa-chevron-up" : "fa-chevron-down"}`;
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

  initializeAssignmentStatusButtons(container, classSectionId);
}

function createAssignmentHTML(assignment, classSectionId) {
  const classSectionState = (assignment.class_sections || []).find(
    (item) => String(item.class_section_id) === String(classSectionId),
  );

  const status = classSectionState?.status || "closed";

  const isActive = status === "active";

  const statusText = isActive ? "Đang bật" : "Đã tắt";

  const statusIcon = isActive ? "fa-toggle-on" : "fa-toggle-off";

  return `
    <div
      class="lesson-assignment-item ${isActive ? "is-active" : "is-closed"}"
      data-assignment-application-id="${escapeHtml(
        assignment.assignment_application_id,
      )}"
      data-class-section-id="${escapeHtml(classSectionId)}"
      data-lesson-id="${escapeHtml(assignment.lesson_id)}"
      data-status="${escapeHtml(status)}"
    >

      <div class="lesson-assignment-main">

        <div class="lesson-assignment-title">

          <span class="lesson-assignment-icon">
            <i class="fa-light fa-file-lines"></i>
          </span>

          <span class="lesson-assignment-title-text">
            ${escapeHtml(assignment.title || "")}
          </span>

        </div>

      </div>

      <div class="lesson-assignment-actions">
                    <button
          type="button"
          class="lesson-assignment-qr-button"
          data-assignment-qr-button
          title="Hiển thị mã QR"
        >
          <i class="fa-light fa-qrcode"></i>
        </button>
        <button
          type="button"
          class="lesson-assignment-status-button ${
            isActive ? "is-active" : "is-closed"
          }"
          data-assignment-status-toggle
          data-status="${escapeHtml(status)}"
          aria-pressed="${isActive}"
          title="${isActive ? "Tắt bài tập" : "Bật bài tập"}"
        >

          <span class="lesson-assignment-status-icon">
            <i class="fa-light ${statusIcon}"></i>
          </span>

          <span class="lesson-assignment-status-text">
            ${statusText}
          </span>

        </button>

      </div>

    </div>
  `;
}

function initializeAssignmentStatusButtons(container, classSectionId) {
  const buttons = container.querySelectorAll("[data-assignment-status-toggle]");

  buttons.forEach((button) => {
    button.addEventListener("click", async () => {
      const item = button.closest(".lesson-assignment-item");

      if (!item) {
        return;
      }

      const applicationId = item.dataset.assignmentApplicationId;

      const currentStatus =
        item.dataset.status || button.dataset.status || "closed";

      const nextStatus = currentStatus === "active" ? "closed" : "active";

      const confirmed = await confirmAssignmentStatusChange(nextStatus);

      if (!confirmed) {
        return;
      }

      await updateAssignmentStatus(
        item,
        button,
        applicationId,
        classSectionId,
        nextStatus,
      );
    });
  });

  container.querySelectorAll(".lesson-assignment-item").forEach((item) => {
    const status = item.dataset.status;

    if (status === "active") {
      initializeAssignmentQrButton(item, classSectionId);
    }
  });
}
function initializeAssignmentQrButton(
  item,
  classSectionId,
) {
  const button =
    item.querySelector(
      "[data-assignment-qr-button]",
    );

  if (!button) {
    return;
  }

  button.addEventListener(
    "click",
    () => {
      const applicationId =
        item.dataset
          .assignmentApplicationId;

      const lessonId =
        item.dataset.lessonId;

      if (
        !applicationId ||
        !classSectionId ||
        !lessonId
      ) {
        console.error(
          "Thiếu dữ liệu để tạo QR.",
          {
            applicationId,
            classSectionId,
            lessonId,
          },
        );

        return;
      }

      showAssignmentQr({
        applicationId,
        classSectionId,
        lessonId,
        title:
          item.querySelector(
            ".lesson-assignment-title-text",
          )?.textContent ||
          "Bài tập",
      });
    },
  );
}
function showAssignmentQr({
  applicationId,
  classSectionId,
  lessonId,
  title,
}) {
  closeAssignmentQr();

  const qrUrl =
    buildAssignmentQrUrl({
      applicationId,
      classSectionId,
      lessonId,
    });

  const overlay =
    document.createElement("div");

  overlay.className =
    "assignment-qr-overlay";

  overlay.id =
    "assignmentQrOverlay";

  overlay.innerHTML = `
    <div
      class="assignment-qr-overlay__backdrop"
      data-assignment-qr-close
    ></div>

    <div
      class="assignment-qr-modal"
      role="dialog"
      aria-modal="true"
      aria-label="Mã QR bài tập"
    >

      <div class="assignment-qr-modal__header">

        <div class="assignment-qr-modal__heading">

          <span class="assignment-qr-modal__icon">
            <i class="fa-light fa-qrcode"></i>
          </span>

          <div class="assignment-qr-modal__heading-content">

            <span class="assignment-qr-modal__label">
              Mã QR bài tập
            </span>

            <span class="assignment-qr-modal__title">
              ${escapeHtml(title)}
            </span>

          </div>

        </div>

        <button
          type="button"
          class="assignment-qr-modal__close"
          data-assignment-qr-close
          aria-label="Đóng"
          title="Đóng"
        >
          <i class="fa-light fa-xmark"></i>
        </button>

      </div>

      <div class="assignment-qr-modal__body">

        <div
          class="assignment-qr-modal__code"
          data-assignment-qr-code
        ></div>

        <div class="assignment-qr-modal__instruction">
          <i class="fa-light fa-mobile-screen-button"></i>
          Quét mã QR để làm bài
        </div>

        <div class="assignment-qr-modal__url">
          ${escapeHtml(qrUrl)}
        </div>

      </div>

    </div>
  `;

  document.body.appendChild(overlay);

  document.body.classList.add(
    "assignment-qr-open",
  );

  const qrElement =
    overlay.querySelector(
      "[data-assignment-qr-code]",
    );

  new QRCode(
    qrElement,
    {
      text: qrUrl,
      width: 260,
      height: 260,
    },
  );

  overlay
    .querySelectorAll(
      "[data-assignment-qr-close]",
    )
    .forEach((element) => {
      element.addEventListener(
        "click",
        closeAssignmentQr,
      );
    });

  document.addEventListener(
    "keydown",
    handleAssignmentQrKeydown,
  );
}

function closeAssignmentQr() {
  const overlay =
    document.getElementById(
      "assignmentQrOverlay",
    );

  if (overlay) {
    overlay.remove();
  }

  document.body.classList.remove(
    "assignment-qr-open",
  );

  document.removeEventListener(
    "keydown",
    handleAssignmentQrKeydown,
  );
}

function handleAssignmentQrKeydown(
  event,
) {
  if (event.key === "Escape") {
    closeAssignmentQr();
  }
}
async function updateAssignmentStatus(
  item,
  button,
  applicationId,
  classSectionId,
  status,
) {
  const originalHtml = button.innerHTML;

  const originalTitle = button.getAttribute("title");

  button.disabled = true;

  button.innerHTML = `
    <span class="lesson-assignment-status-icon">
      <i class="fa-light fa-spinner fa-spin"></i>
    </span>

    <span class="lesson-assignment-status-text">
      Đang cập nhật...
    </span>
  `;

  try {
    const response = await fetch(
      `/teacher/assignment/applications/${encodeURIComponent(
        applicationId,
      )}/class-sections/${encodeURIComponent(classSectionId)}/status`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify({
          status,
        }),
      },
    );

    const contentType = response.headers.get("content-type");

    const responseText = await response.text();

    if (!contentType || !contentType.includes("application/json")) {
      throw new Error(
        `Server không trả JSON. HTTP ${response.status}: ${responseText}`,
      );
    }

    const result = JSON.parse(responseText);

    if (!response.ok || result.success !== true) {
      throw new Error(
        result.message || "Không thể cập nhật trạng thái bài tập.",
      );
    }

    item.dataset.status = status;

    button.dataset.status = status;

    const isActive = status === "active";

    button.classList.toggle("is-active", isActive);

    button.classList.toggle("is-closed", !isActive);

    button.setAttribute("aria-pressed", String(isActive));

    button.setAttribute("title", isActive ? "Tắt bài tập" : "Bật bài tập");

    button.innerHTML = `
  <span class="lesson-assignment-status-icon">
    <i class="fa-light ${isActive ? "fa-toggle-on" : "fa-toggle-off"}"></i>
  </span>

  <span class="lesson-assignment-status-text">
    ${isActive ? "Đang bật" : "Đã tắt"}
  </span>
`;

    updateAssignmentQr(item, isActive);
  } catch (errorObject) {
    console.error("UPDATE ASSIGNMENT STATUS ERROR:", errorObject);

    button.innerHTML = originalHtml;

    if (originalTitle) {
      button.setAttribute("title", originalTitle);
    }

    showAssignmentError(
      item,
      errorObject.message || "Không thể cập nhật trạng thái.",
    );
  } finally {
    button.disabled = false;
  }
}
function buildAssignmentQrUrl({
  applicationId,
  classSectionId,
  lessonId,
}) {
  const url = new URL(
    "/student/assignment/qr",
    window.location.origin,
  );

  url.searchParams.set(
    "assignment_application_id",
    applicationId,
  );

  url.searchParams.set(
    "class_section_id",
    classSectionId,
  );

  url.searchParams.set(
    "lesson_id",
    lessonId,
  );

  url.searchParams.set(
    "QR-CODE",
    "TRUE",
  );

  return url.toString();
}
async function confirmAssignmentStatusChange(nextStatus) {
  const message =
    nextStatus === "active"
      ? "Bật bài tập cho lớp học phần này?"
      : "Tắt bài tập cho lớp học phần này?";

  return window.confirm(message);
}

function showAssignmentError(item, message) {
  let error = item.querySelector(".assignment-status-error");

  if (!error) {
    error = document.createElement("div");

    error.className = "assignment-status-error";

    item.appendChild(error);
  }

  error.textContent = message;

  window.setTimeout(() => {
    if (error.parentNode) {
      error.remove();
    }
  }, 4000);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
