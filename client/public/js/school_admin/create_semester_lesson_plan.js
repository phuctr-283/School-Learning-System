function initSemesterLessonPlanForm() {
  const form = document.getElementById("semesterLessonPlanCreateForm");

  if (!form) {
    return;
  }

  /* =========================================
     ELEMENTS
  ========================================== */

  const academicYearSelect = document.getElementById("academicYearId");

  const semesterCards = form.querySelectorAll("[data-semester-card]");

  const semesterLessonInputs = form.querySelectorAll(
    'input[name$="[total_lessons]"]',
  );

  const summaryAcademicYear = document.getElementById("summaryAcademicYear");

  const summarySemester = document.getElementById("summarySemester");

  const summaryLessons = document.getElementById("summaryLessons");

  /* =========================================
     SEMESTER CONTENT DATA
  ========================================== */

  const semesterContents = Array.isArray(window.semesterContents)
    ? window.semesterContents
    : [];

  /* =========================================
     GET SEMESTER NUMBER
  ========================================== */

  function getSemesterNumber(input) {
    const card = input.closest("[data-semester-card]");

    if (!card) {
      return null;
    }

    return card.dataset.semesterCard;
  }

  /* =========================================
     FIND SEMESTER
     
     Tìm SemesterContentDTO theo:
     academicYearId
     +
     semesterNumber
  ========================================== */

  function findSemester(academicYearId, semesterNumber) {
    return semesterContents.find(
      (semester) =>
        String(semester.academicYearId) === String(academicYearId) &&
        String(semester.semesterNumber) === String(semesterNumber),
    );
  }

  /* =========================================
     GET ENTERED SEMESTERS
  ========================================== */

  function getEnteredSemesters() {
    const semesters = [];

    semesterLessonInputs.forEach((input) => {
      if (input.disabled) {
        return;
      }

      const value = Number(input.value || 0);

      if (value > 0) {
        const semesterNumber = getSemesterNumber(input);

        if (semesterNumber) {
          semesters.push({
            semesterNumber: Number(semesterNumber),

            totalLessons: value,
          });
        }
      }
    });

    return semesters;
  }

  /* =========================================
     UPDATE ACADEMIC YEAR SUMMARY
  ========================================== */

  function updateAcademicYearSummary() {
    if (!summaryAcademicYear) {
      return;
    }

    const selectedOption = academicYearSelect?.selectedOptions?.[0];

    if (academicYearSelect?.value && selectedOption) {
      summaryAcademicYear.textContent = selectedOption.textContent.trim();

      return;
    }

    summaryAcademicYear.textContent = "Chưa chọn";
  }

  /* =========================================
     UPDATE SEMESTER CARDS
     
     Khi chọn năm học:
     
     2025 - 2026
       ↓
     tìm semester theo academicYearId
       ↓
     hiện đúng HK1 / HK2 / HK3
  ========================================== */

  function updateSemesterCards() {
    const academicYearId = academicYearSelect?.value;

    semesterCards.forEach((card) => {
      const semesterNumber = card.dataset.semesterCard;

      const semester = findSemester(academicYearId, semesterNumber);

      const nameElement = card.querySelector("[data-semester-name]");

      const lessonInput = card.querySelector('input[name$="[total_lessons]"]');

      /* ================================
           Chưa chọn năm học
        ================================= */

      if (!academicYearId) {
        card.style.display = "";

        if (nameElement) {
          nameElement.textContent = "Chưa chọn năm học";
        }

        if (lessonInput) {
          lessonInput.disabled = true;
          lessonInput.value = "";
        }

        return;
      }

      /* ================================
           Không có semester
        ================================= */

      if (!semester) {
        card.style.display = "none";

        if (lessonInput) {
          lessonInput.disabled = true;
          lessonInput.value = "";
        }

        return;
      }

      /* ================================
           Có semester
        ================================= */

      card.style.display = "";

      if (nameElement) {
        nameElement.textContent = semester.name;
      }

      if (lessonInput) {
        lessonInput.disabled = false;
      }
    });
  }

  /* =========================================
     UPDATE SEMESTER SUMMARY
  ========================================== */

  function updateSemesterSummary() {
    if (!summarySemester) {
      return;
    }

    const semesters = getEnteredSemesters();

    if (!semesters.length) {
      summarySemester.textContent = "Chưa cấu hình";

      return;
    }

    const semesterNames = semesters.map((item) => {
      const semester = findSemester(
        academicYearSelect.value,
        item.semesterNumber,
      );

      return semester ? semester.name : `Học kỳ ${item.semesterNumber}`;
    });

    summarySemester.textContent = semesterNames.join(", ");
  }

  /* =========================================
     UPDATE TOTAL LESSONS
  ========================================== */

  function updateTotalLessonsSummary() {
    if (!summaryLessons) {
      return;
    }

    const semesters = getEnteredSemesters();

    const totalLessons = semesters.reduce(
      (total, semester) => total + semester.totalLessons,
      0,
    );

    summaryLessons.textContent = `${totalLessons} buổi`;
  }

  /* =========================================
     UPDATE CARD STATE
  ========================================== */

  function updateSemesterCardState(input) {
    const card = input.closest("[data-semester-card]");

    if (!card) {
      return;
    }

    const value = Number(input.value || 0);

    card.classList.toggle("has-value", value > 0);
  }

  /* =========================================
     UPDATE SUMMARY
  ========================================== */

  function updateSummary() {
    updateAcademicYearSummary();

    updateSemesterSummary();

    updateTotalLessonsSummary();

    semesterLessonInputs.forEach((input) => {
      updateSemesterCardState(input);
    });
  }

  /* =========================================
     ACADEMIC YEAR EVENT
  ========================================== */

  academicYearSelect?.addEventListener("change", () => {
    updateSemesterCards();

    updateSummary();
  });

  /* =========================================
     INPUT EVENTS
  ========================================== */

  semesterLessonInputs.forEach((input) => {
    input.addEventListener("input", () => {
      updateSemesterCardState(input);

      updateSemesterSummary();

      updateTotalLessonsSummary();
    });

    input.addEventListener("change", () => {
      updateSemesterCardState(input);

      updateSemesterSummary();

      updateTotalLessonsSummary();
    });
  });

  /* =========================================
     FORM VALIDATION
  ========================================== */

  form.addEventListener("submit", (event) => {
    /* ================================
         Kiểm tra năm học
      ================================= */

    if (!academicYearSelect?.value) {
      event.preventDefault();

      academicYearSelect?.focus();

      return;
    }

    /* ================================
         Kiểm tra semester
      ================================= */

    const enteredSemesters = getEnteredSemesters();

    if (!enteredSemesters.length) {
      event.preventDefault();

      const firstAvailableInput = Array.from(semesterLessonInputs).find(
        (input) => !input.disabled,
      );

      firstAvailableInput?.focus();

      return;
    }

    /* ================================
         Validate total lessons
      ================================= */

    for (const input of semesterLessonInputs) {
      if (input.disabled) {
        continue;
      }

      if (input.value === "") {
        continue;
      }

      const value = Number(input.value);

      if (!Number.isInteger(value) || value < 1 || value > 100) {
        event.preventDefault();

        input.focus();

        return;
      }
    }
  });

  /* =========================================
     INITIALIZE
  ========================================== */

  updateSemesterCards();

  updateSummary();
}

/* =========================================
   DOM READY
========================================== */

document.addEventListener("DOMContentLoaded", () => {
  initSemesterLessonPlanForm();
});
