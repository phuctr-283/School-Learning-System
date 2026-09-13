function initLessonCreateForm() {
  const form = document.getElementById("lessonCreateForm");

  if (!form) {
    return;
  }

  /* =====================================================
       ELEMENTS
    ====================================================== */

  const modeOptions = form.querySelectorAll("[data-mode-option]");

  const singleSection = document.getElementById("singleLessonSection");

  const multipleSection = document.getElementById("multipleLessonSection");

  const lessonNumber = document.getElementById("lessonNumber");

  const lessonNumberStart = document.getElementById("lessonNumberStart");

  const lessonNumberEnd = document.getElementById("lessonNumberEnd");

  const rangeText = document.getElementById("lessonRangeText");

  const rangeCount = document.getElementById("lessonRangeCount");

  const submitText = document.getElementById("submitText");

  const infoExample = document.getElementById("lessonInfoExample");

  /* =====================================================
       REVIEW
    ====================================================== */

  const lessonReview = document.getElementById("lessonReview");

  const reviewLessonNumber = document.getElementById("reviewLessonNumber");

  const reviewLessonCount = document.getElementById("reviewLessonCount");

  const reviewLessonRange = document.getElementById("reviewLessonRange");

  const reviewLessonRangeCount = document.getElementById(
    "reviewLessonRangeCount",
  );

  const reviewStatus = document.getElementById("lessonReviewStatus");

  /* =====================================================
       CREATE MODE
    ====================================================== */

  function getCreateMode() {
    const checked = form.querySelector('input[name="create_mode"]:checked');

    return checked ? checked.value : "single";
  }

  /* =====================================================
       UPDATE REVIEW
    ====================================================== */

  function updateReview() {
    if (!lessonReview) {
      return;
    }

    const mode = getCreateMode();

    /* ================================================
           SINGLE
        ================================================= */

    if (mode === "single") {
      lessonReview.classList.remove("is-multiple");

      const number = Number(lessonNumber?.value);

      if (!number || number < 1) {
        lessonReview.classList.remove("is-complete");

        if (reviewLessonNumber) {
          reviewLessonNumber.textContent = "Chưa nhập";
        }

        if (reviewLessonCount) {
          reviewLessonCount.textContent = "0 buổi";
        }

        if (reviewStatus) {
          reviewStatus.textContent = "Chưa hoàn tất";
        }

        return;
      }

      lessonReview.classList.add("is-complete");

      if (reviewLessonNumber) {
        reviewLessonNumber.textContent = `Buổi ${number}`;
      }

      if (reviewLessonCount) {
        reviewLessonCount.textContent = "1 buổi";
      }

      if (reviewStatus) {
        reviewStatus.textContent = "Sẵn sàng tạo";
      }

      return;
    }

    /* ================================================
           MULTIPLE
        ================================================= */

    lessonReview.classList.add("is-multiple");

    const start = Number(lessonNumberStart?.value);

    const end = Number(lessonNumberEnd?.value);

    if (!start || !end || start < 1 || end < start) {
      lessonReview.classList.remove("is-complete");

      if (reviewLessonRange) {
        reviewLessonRange.textContent = "Chưa xác định";
      }

      if (reviewLessonRangeCount) {
        reviewLessonRangeCount.textContent = "0 buổi";
      }

      if (reviewStatus) {
        reviewStatus.textContent = "Chưa hoàn tất";
      }

      return;
    }

    const count = end - start + 1;

    lessonReview.classList.add("is-complete");

    if (reviewLessonRange) {
      reviewLessonRange.textContent = `Buổi ${start} → Buổi ${end}`;
    }

    if (reviewLessonRangeCount) {
      reviewLessonRangeCount.textContent = `${count} buổi`;
    }

    if (reviewStatus) {
      reviewStatus.textContent = "Sẵn sàng tạo";
    }
  }

  /* =====================================================
       UPDATE RANGE
    ====================================================== */

  function updateRange() {
    const start = Number(lessonNumberStart?.value);

    const end = Number(lessonNumberEnd?.value);

    if (!start || !end || start < 1 || end < start || end > 20) {
      if (rangeText) {
        rangeText.textContent = "Chưa xác định khoảng buổi học";
      }

      if (rangeCount) {
        rangeCount.textContent = "0 buổi";
      }

      if (infoExample) {
        infoExample.innerHTML = `
                    <span>Ví dụ:</span>
                    <code>Buổi 1 → Buổi 10</code>
                    <strong>10 buổi</strong>
                `;
      }

      updateReview();

      return;
    }

    const count = end - start + 1;

    if (rangeText) {
      rangeText.textContent = `Buổi ${start} → Buổi ${end}`;
    }

    if (rangeCount) {
      rangeCount.textContent = `${count} buổi`;
    }

    if (infoExample) {
      infoExample.innerHTML = `
                <span>Đang tạo:</span>
                <code>Buổi ${start} → Buổi ${end}</code>
                <strong>${count} buổi</strong>
            `;
    }

    updateReview();
  }

  /* =====================================================
       UPDATE MODE
    ====================================================== */

  function updateMode() {
    const mode = getCreateMode();

    modeOptions.forEach((option) => {
      const input = option.querySelector('input[type="radio"]');

      option.classList.toggle("is-active", input?.checked);
    });

    if (mode === "single") {
      singleSection?.classList.add("is-active");

      multipleSection?.classList.remove("is-active");

      if (submitText) {
        submitText.textContent = "Tạo buổi học";
      }

      updateReview();

      return;
    }

    singleSection?.classList.remove("is-active");

    multipleSection?.classList.add("is-active");

    if (submitText) {
      submitText.textContent = "Tạo các buổi học";
    }

    updateRange();
  }

  /* =====================================================
       MODE EVENTS
    ====================================================== */

  modeOptions.forEach((option) => {
    option.addEventListener("click", () => {
      const input = option.querySelector('input[type="radio"]');

      if (!input) {
        return;
      }

      input.checked = true;

      updateMode();
    });
  });

  /* =====================================================
       SINGLE INPUT
    ====================================================== */

  lessonNumber?.addEventListener("input", updateReview);

  /* =====================================================
       MULTIPLE INPUT
    ====================================================== */

  lessonNumberStart?.addEventListener("input", updateRange);

  lessonNumberEnd?.addEventListener("input", updateRange);

  /* =====================================================
       SUBMIT
    ====================================================== */

  form.addEventListener("submit", (event) => {
    const mode = getCreateMode();

    /* ============================================
               SINGLE
    ============================================= */

    if (mode === "single") {
      const number = Number(lessonNumber?.value);

      if (!number || number < 1) {
        event.preventDefault();

        lessonNumber?.focus();

        return;
      }
    }

    /* ============================================
               MULTIPLE
    ============================================= */

    if (mode === "multiple") {
      const start = Number(lessonNumberStart?.value);

      const end = Number(lessonNumberEnd?.value);

      if (!start || !end) {
        event.preventDefault();

        if (!start) {
          lessonNumberStart?.focus();
        } else {
          lessonNumberEnd?.focus();
        }

        return;
      }

      if (end < start) {
        event.preventDefault();

        lessonNumberEnd?.focus();

        return;
      }
    }
  });

  /* =====================================================
       INITIALIZE
    ====================================================== */

  updateMode();
}

document.addEventListener("DOMContentLoaded", () => {
  initLessonCreateForm();
});
