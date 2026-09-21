document.addEventListener("DOMContentLoaded", initializeLessonOpening);

function initializeLessonOpening() {
  const page = document.querySelector(".lesson-opening-page");

  if (!page) {
    return;
  }

  initializeAcademicYear();
  initializeSemester();
  initializeGroups();
  initializeLessons();
  initializeApplyAssignment();
}

function initializeAcademicYear() {
  const select = document.getElementById("academicYearSelect");

  if (!select) {
    return;
  }

  select.addEventListener("change", handleAcademicYearChange);
}

function initializeSemester() {
  document
    .querySelectorAll(".lesson-opening-semester-radio")
    .forEach((radio) => {
      radio.addEventListener("change", handleSemesterChange);
    });
}

function initializeGroups() {
  const selectAll = document.getElementById("selectAllGroups");

  if (selectAll) {
    selectAll.addEventListener("change", handleSelectAllGroups);
  }

  const groupList = document.getElementById("groupList");

  if (groupList) {
    groupList.addEventListener("change", handleGroupChange);
  }
}

function initializeLessons() {
  const lessonList = document.getElementById("lessonList");

  if (!lessonList) {
    return;
  }

  lessonList.addEventListener("change", handleLessonChange);
}

function initializeApplyAssignment() {
  const button = document.getElementById("applyAssignmentButton");

  if (!button) {
    return;
  }

  button.addEventListener("click", handleApplyAssignment);
}
function handleAcademicYearChange(event) {
  const academicYearId = event.target.value;

  resetSemester();
  resetGroups();
  resetLessons();

  if (!academicYearId) {
    return;
  }

  const semesterList = document.getElementById("semesterList");

  if (semesterList) {
    semesterList.hidden = false;
  }

  document.querySelectorAll(".lesson-opening-semester-item").forEach((item) => {
    item.hidden = item.dataset.academicYearId !== academicYearId;
  });
}

async function handleSemesterChange(event) {
  const academicYearId = document.getElementById("academicYearSelect")?.value;

  const semesterId = event.target.value;

  const page = document.querySelector(".lesson-opening-page");

  const subjectId = page?.dataset.subjectId;

  resetGroups();
  resetLessons();

  if (!academicYearId || !semesterId || !subjectId) {
    return;
  }

  await Promise.all([
    loadClassSections(academicYearId, semesterId, subjectId),

    loadLessonOpenings(academicYearId, semesterId, subjectId),
  ]);
}

async function loadClassSections(academicYearId, semesterId, subjectId) {
  const params = new URLSearchParams({
    academic_year_id: academicYearId,

    semester_id: semesterId,

    subject_id: subjectId,
  });

  try {
    const response = await fetch(
      `/teacher/assignment/lesson-opening/class-sections?${params}`,
      {
        headers: {
          Accept: "application/json",
        },
      },
    );

    const result = await response.json();

    if (!response.ok || !result.success) {
      throw new Error(result.message || "Không thể tải nhóm lớp học phần.");
    }

    console.log("CLASS SECTION:", result);

    renderClassSections(result.data || []);
  } catch (error) {
    console.error("LOAD CLASS SECTIONS ERROR:", error);

    renderClassSections([]);
  }
}

async function loadLessonOpenings(academicYearId, semesterId, subjectId) {
  const params = new URLSearchParams({
    academic_year_id: academicYearId,

    semester_id: semesterId,

    subject_id: subjectId,
  });

  try {
    const response = await fetch(
      `/teacher/assignment/lesson-opening/lessons?${params}`,
      {
        headers: {
          Accept: "application/json",
        },
      },
    );

    const result = await response.json();

    if (!response.ok || !result.success) {
      throw new Error(result.message || "Không thể tải buổi học.");
    }

    console.log("LESSON:", result);

    renderLessonOpenings(result.data || []);
  } catch (error) {
    console.error("LOAD LESSON OPENINGS ERROR:", error);

    renderLessonOpenings([]);
  }
}

function renderClassSections(classSections) {
  const section = document.getElementById("classSectionGroup");

  const list = document.getElementById("groupList");

  const selectAll = document.getElementById("selectAllGroups");

  if (!section || !list) {
    return;
  }

  list.innerHTML = "";

  if (selectAll) {
    selectAll.checked = false;
  }

  classSections.forEach((classSection) => {
    const classSectionId =
      classSection.class_section_id ?? classSection.classSectionId;

    const groupNumber = classSection.group_number ?? classSection.groupNumber;

    const subjectName =
      classSection.subject_name ?? classSection.subjectName ?? "";

    const status = classSection.status ?? "";

    const label = document.createElement("label");

    label.className = "lesson-opening-group-item";

    label.innerHTML = `
        <input
          type="checkbox"
          name="classSectionIds"
          value="${escapeHtml(classSectionId)}"
          class="lesson-opening-group-checkbox"
        >

        <span class="lesson-opening-group-content">

          <span class="lesson-opening-group-name">
            Nhóm ${escapeHtml(groupNumber)}
          </span>

          <span class="lesson-opening-group-subject">
            ${escapeHtml(subjectName)}
          </span>

        </span>

        <span class="lesson-opening-group-status">
          ${escapeHtml(status)}
        </span>
      `;

    list.appendChild(label);
  });

  section.hidden = classSections.length === 0;

  updateActionState();
}

function renderLessonOpenings(lessonOpenings) {
  const section = document.getElementById("lessonSection");

  const list = document.getElementById("lessonList");

  if (!section || !list) {
    return;
  }

  list.innerHTML = "";

  lessonOpenings.forEach((lesson) => {
    const lessonId = lesson.lesson_id ?? lesson.lessonId;

    const lessonNumber = lesson.lesson_number ?? lesson.lessonNumber;

    const lessonName =
      lesson.lesson_name ?? lesson.lessonName ?? `Buổi ${lessonNumber}`;

    const label = document.createElement("label");

    label.className = "lesson-opening-lesson-item";

    label.innerHTML = `
        <input
          type="radio"
          name="lessonId"
          value="${escapeHtml(lessonId)}"
          class="lesson-opening-lesson-radio"
        >

        <span class="lesson-opening-lesson-content">

          <span class="lesson-opening-lesson-number">
            ${escapeHtml(lessonNumber)}
          </span>

          <span class="lesson-opening-lesson-info">

            <span class="lesson-opening-lesson-name">
              ${escapeHtml(lessonName)}
            </span>

            <span class="lesson-opening-lesson-id">
              ${escapeHtml(lessonId)}
            </span>

          </span>

        </span>
      `;

    list.appendChild(label);
  });

  section.hidden = lessonOpenings.length === 0;

  updateActionState();
}

function handleSelectAllGroups(event) {
  document
    .querySelectorAll(".lesson-opening-group-checkbox")
    .forEach((checkbox) => {
      checkbox.checked = event.target.checked;
    });

  updateActionState();
}

function handleGroupChange() {
  const checkboxes = [
    ...document.querySelectorAll(".lesson-opening-group-checkbox"),
  ];

  const selected = checkboxes.filter((checkbox) => checkbox.checked);

  const selectAll = document.getElementById("selectAllGroups");

  if (selectAll) {
    selectAll.checked =
      checkboxes.length > 0 && selected.length === checkboxes.length;
  }

  updateActionState();
}

function handleLessonChange() {
  updateActionState();
}

function updateActionState() {
  const groups = document.querySelectorAll(
    ".lesson-opening-group-checkbox:checked",
  );

  const lesson = document.querySelector(
    ".lesson-opening-lesson-radio:checked",
  );

  const action = document.getElementById(
    "lessonOpeningAction",
  );

  const button = document.getElementById(
    "applyAssignmentButton",
  );

  if (!action || !button) {
    return;
  }

  if (button.dataset.applied === "true") {
    action.hidden = false;
    button.disabled = true;
    return;
  }

  const enabled =
    groups.length > 0 && !!lesson;

  action.hidden = !enabled;
  button.disabled = !enabled;
}
function updateAppliedState(data) {
  const button = document.getElementById(
    "applyAssignmentButton",
  );

  if (!button) {
    return;
  }

  button.dataset.applied = "true";
  button.disabled = true;
  button.classList.remove("is-loading");
  button.classList.add("is-applied");

  const text = button.querySelector("span");

  if (text) {
    text.textContent = "Đã áp dụng bài tập";
  }
}
async function handleApplyAssignment() {
  const page = document.querySelector(
    ".lesson-opening-page",
  );

  const lesson = document.querySelector(
    ".lesson-opening-lesson-radio:checked",
  );

  const groups = [
    ...document.querySelectorAll(
      ".lesson-opening-group-checkbox:checked",
    ),
  ];

  if (!page || !lesson) {
    return;
  }

  if (groups.length === 0) {
    return;
  }

  const assignmentId =
    page.dataset.assignmentId;

  console.log(
    "ASSIGNMENT ID:",
    assignmentId,
  );

  const lessonId = lesson.value;

  const classSectionIds = groups
    .map((group) => group.value)
    .filter(Boolean);

  if (!assignmentId) {
    alert("Không xác định được bài tập.");
    return;
  }

  if (!lessonId) {
    alert("Không xác định được buổi học.");
    return;
  }

  if (classSectionIds.length === 0) {
    alert(
      "Vui lòng chọn ít nhất một nhóm lớp học phần.",
    );
    return;
  }

  const button = document.getElementById(
    "applyAssignmentButton",
  );

  if (button) {
    button.disabled = true;
    button.classList.add("is-loading");
  }

  try {
    const response = await fetch(
      "/teacher/assignment/lesson-opening/apply-assignment",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          assignment_id: assignmentId,
          lesson_id: lessonId,
          class_section_ids: classSectionIds,
          max_attempts: 1,
        }),
      },
    );

    const contentType =
      response.headers.get("content-type") || "";

    if (!contentType.includes("application/json")) {
      const text = await response.text();

      console.error(
        "NON JSON RESPONSE:",
        text,
      );

      throw new Error(
        `Server trả về dữ liệu không hợp lệ (${response.status}).`,
      );
    }

    const result = await response.json();

    if (!response.ok || !result.success) {
      throw new Error(
        result.message ||
          "Không thể áp dụng bài tập.",
      );
    }

    console.log(
      "APPLY ASSIGNMENT SUCCESS:",
      result,
    );

    updateAppliedState(result.data);
  } catch (error) {
    console.error(
      "APPLY ASSIGNMENT ERROR:",
      error,
    );

    alert(
      error.message ||
        "Không thể áp dụng bài tập.",
    );

    if (button) {
      button.disabled = false;
    }
  } finally {
    if (button) {
      button.classList.remove("is-loading");
    }

    updateActionState();
  }
}

function resetSemester() {
  document
    .querySelectorAll(".lesson-opening-semester-radio")
    .forEach((radio) => {
      radio.checked = false;
    });

  const list = document.getElementById("semesterList");

  if (list) {
    list.hidden = true;
  }

  document.querySelectorAll(".lesson-opening-semester-item").forEach((item) => {
    item.hidden = true;
  });
}

function resetGroups() {
  const section = document.getElementById("classSectionGroup");

  const list = document.getElementById("groupList");

  const selectAll = document.getElementById("selectAllGroups");

  if (section) {
    section.hidden = true;
  }

  if (list) {
    list.innerHTML = "";
  }

  if (selectAll) {
    selectAll.checked = false;
  }
}

function resetLessons() {
  const section =
    document.getElementById("lessonSection");

  const list =
    document.getElementById("lessonList");

  const action =
    document.getElementById("lessonOpeningAction");

  const button =
    document.getElementById("applyAssignmentButton");

  if (section) {
    section.hidden = true;
  }

  if (list) {
    list.innerHTML = "";
  }

  if (action) {
    action.hidden = true;
  }

  if (button) {
    button.disabled = true;
    button.dataset.applied = "false";
    button.classList.remove("is-applied");
    button.classList.remove("is-loading");

    const text = button.querySelector("span");

    if (text) {
      text.textContent = "Áp dụng bài tập";
    }
  }
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
