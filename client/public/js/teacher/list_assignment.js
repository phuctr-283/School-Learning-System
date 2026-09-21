document.addEventListener("DOMContentLoaded", () => {
  initAssignmentList();
});

function initAssignmentList() {
  const rows = document.querySelectorAll(".assignment-row");
  const searchInput = document.getElementById("searchAssignment");
  const filterEmptyRow = document.getElementById("assignment-filter-empty");

  if (!searchInput || !rows.length) {
    return;
  }

  let searchKeyword = "";

  searchInput.addEventListener("input", () => {
    searchKeyword = normalizeText(searchInput.value);

    filterAssignments(rows, searchKeyword, filterEmptyRow);
  });
}

function normalizeText(value) {
  return String(value ?? "")
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

function filterAssignments(rows, searchKeyword, filterEmptyRow) {
  let visibleCount = 0;

  rows.forEach((row) => {
    const rowText = normalizeText(row.dataset.searchText || row.textContent);

    const shouldShow = !searchKeyword || rowText.includes(searchKeyword);

    row.hidden = !shouldShow;

    if (shouldShow) {
      visibleCount += 1;
    }
  });

  if (filterEmptyRow) {
    filterEmptyRow.hidden = visibleCount > 0;
  }
}
document.addEventListener("DOMContentLoaded", initializeLessonOpening);

function initializeLessonOpening() {
  const overlay = document.getElementById("lessonOpeningOverlay");

  if (!overlay) {
    return;
  }

  const trigger = document.querySelector("[data-lesson-opening-trigger]");

  if (trigger) {
    trigger.addEventListener("click", openLessonOpening);
  }

  document
    .querySelectorAll("[data-lesson-opening-close]")
    .forEach((element) => {
      element.addEventListener("click", closeLessonOpening);
    });

  initializeAcademicYear();
  initializeSemester();
  initializeSubject();
  initializeGroups();
  initializeLessons();
}

function openLessonOpening() {
  const overlay = document.getElementById("lessonOpeningOverlay");

  if (!overlay) {
    return;
  }

  overlay.hidden = false;

  document.body.classList.add("lesson-opening-overlay-open");
}

function closeLessonOpening() {
  const overlay = document.getElementById("lessonOpeningOverlay");

  if (!overlay) {
    return;
  }

  overlay.hidden = true;

  document.body.classList.remove("lesson-opening-overlay-open");
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

function initializeSubject() {
  const select = document.getElementById("subjectSelect");

  if (!select) {
    return;
  }

  select.addEventListener("change", handleSubjectChange);
}

function initializeGroups() {
  const selectAll = document.getElementById("selectAllGroups");

  if (!selectAll) {
    return;
  }

  selectAll.addEventListener("change", handleSelectAllGroups);

  document
    .getElementById("groupList")
    ?.addEventListener("change", handleGroupChange);
}

function initializeLessons() {
  document
    .getElementById("lessonList")
    ?.addEventListener("change", handleLessonChange);
}

function handleAcademicYearChange(event) {
  const academicYearId = event.target.value;

  resetSemester();

  resetSubject();

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

  resetSubject();

  resetGroups();

  resetLessons();

  if (!academicYearId || !semesterId) {
    return;
  }

  await loadSubjects(academicYearId, semesterId);
}

async function loadSubjects(academicYearId, semesterId) {
  const subjectSelect = document.getElementById("subjectSelect");

  if (!subjectSelect) {
    return;
  }

  subjectSelect.disabled = true;

  subjectSelect.innerHTML = `
      <option value="">
        Đang tải môn học...
      </option>
    `;

  try {
    const params = new URLSearchParams({
      academic_year_id: academicYearId,

      semester_id: semesterId,
    });

    const response = await fetch(
      `/teacher/lesson-opening/subjects?${params.toString()}`,
      {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      },
    );

    const result = await response.json();

    if (!response.ok || !result.success) {
      throw new Error(result.message || "Không thể tải môn học.");
    }

    renderSubjects(result.data || []);
  } catch (error) {
    subjectSelect.innerHTML = `
        <option value="">
          Không thể tải môn học
        </option>
      `;

    console.error("LOAD SUBJECTS ERROR:", error);
  }
}

function renderSubjects(subjects) {
  const select = document.getElementById("subjectSelect");

  if (!select) {
    return;
  }

  select.innerHTML = `
      <option value="">
        Chọn môn học
      </option>
    `;

  subjects.forEach((subject) => {
    const option = document.createElement("option");

    option.value = subject.subjectId;

    option.textContent = subject.subjectName;

    select.appendChild(option);
  });

  select.disabled = subjects.length === 0;
}

async function handleSubjectChange(event) {
  const subjectId = event.target.value;

  const academicYearId = document.getElementById("academicYearSelect")?.value;

  const semesterId = document.querySelector(
    ".lesson-opening-semester-radio:checked",
  )?.value;

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
      `/teacher/lesson-opening/class-sections?${params.toString()}`,
      {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      },
    );

    const result = await response.json();

    if (!response.ok || !result.success) {
      throw new Error(result.message || "Không thể tải nhóm lớp học phần.");
    }

    renderClassSections(result.data || []);
  } catch (error) {
    console.error("LOAD CLASS SECTIONS ERROR:", error);
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
      `/teacher/lesson-opening/lessons?${params.toString()}`,
      {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      },
    );

    const result = await response.json();

    if (!response.ok || !result.success) {
      throw new Error(result.message || "Không thể tải buổi học.");
    }

    renderLessonOpenings(result.data || []);
  } catch (error) {
    console.error("LOAD LESSON OPENINGS ERROR:", error);
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
    const label = document.createElement("label");

    label.className = "lesson-opening-group-item";

    label.innerHTML = `
          <input
            type="checkbox"
            name="classSectionIds"
            value="${escapeHtml(classSection.classSectionId)}"
            class="lesson-opening-group-checkbox"
          >

          <span class="lesson-opening-group-content">

            <span class="lesson-opening-group-name">
              Nhóm ${escapeHtml(classSection.groupNumber)}
            </span>

            <span class="lesson-opening-group-subject">
              ${escapeHtml(classSection.subjectName)}
            </span>

          </span>

          <span class="lesson-opening-group-status">
            ${escapeHtml(classSection.status)}
          </span>
        `;

    list.appendChild(label);
  });

  section.hidden = classSections.length === 0;
}

function renderLessonOpenings(lessonOpenings) {
  const section = document.getElementById("lessonSection");

  const list = document.getElementById("lessonList");

  if (!section || !list) {
    return;
  }

  list.innerHTML = "";

  lessonOpenings.forEach((lesson) => {
    const label = document.createElement("label");

    label.className = "lesson-opening-lesson-item";

    label.innerHTML = `
          <input
            type="radio"
            name="lessonId"
            value="${escapeHtml(lesson.lessonId)}"
            class="lesson-opening-lesson-radio"
            data-status="${escapeHtml(lesson.status)}"
          >

          <span class="lesson-opening-lesson-content">

            <span class="lesson-opening-lesson-number">
              ${escapeHtml(lesson.lessonNumber)}
            </span>

            <span class="lesson-opening-lesson-info">

              <span class="lesson-opening-lesson-name">
                ${escapeHtml(
                  lesson.lessonName || `Buổi ${lesson.lessonNumber}`,
                )}
              </span>

              <span class="lesson-opening-lesson-id">
                ${escapeHtml(lesson.lessonId)}
              </span>

            </span>

            <span
              class="
                lesson-opening-lesson-status
                lesson-opening-lesson-status--${escapeHtml(lesson.status)}
              "
            >
              ${getLessonStatusText(lesson.status)}
            </span>

          </span>
        `;

    list.appendChild(label);
  });

  section.hidden = lessonOpenings.length === 0;
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

  const checked = checkboxes.filter((checkbox) => checkbox.checked);

  const selectAll = document.getElementById("selectAllGroups");

  if (selectAll) {
    selectAll.checked =
      checkboxes.length > 0 && checked.length === checkboxes.length;
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

  const lesson = document.querySelector(".lesson-opening-lesson-radio:checked");

  const action = document.getElementById("lessonOpeningAction");

  const button = document.getElementById("openLessonButton");

  if (!action || !button) {
    return;
  }

  const enabled = groups.length > 0 && !!lesson;

  action.hidden = !enabled;

  button.disabled = !enabled;

  if (!lesson) {
    return;
  }

  if (lesson.dataset.status === "open") {
    button.innerHTML = `
        <i class="fa-light fa-power-off"></i>
        <span>Đóng buổi học</span>
      `;
  } else {
    button.innerHTML = `
        <i class="fa-light fa-power-off"></i>
        <span>Mở buổi học</span>
      `;
  }
}
