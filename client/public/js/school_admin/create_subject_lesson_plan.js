function initSubjectLessonPlanRules() {
  const form = document.getElementById("subjectLessonPlanCreateForm");

  if (!form) {
    return;
  }

  /* =========================================================
       CONFIG
    ========================================================= */

  const ruleIndexes = {
    theory: 1,
    practice: 1,
  };

  /* =========================================================
       HELPERS
    ========================================================= */

  function getRuleList(type) {
    return form.querySelector(`[data-rule-list="${type}"]`);
  }

  function getRules(type) {
    const list = getRuleList(type);

    if (!list) {
      return [];
    }

    return Array.from(list.querySelectorAll("[data-rule-item]"));
  }

  function getRuleCount(type) {
    return getRules(type).length;
  }

  /* =========================================================
       SEMESTER
    ========================================================= */

  function initSemesterSelection() {
    const semesterOptions = form.querySelectorAll("[data-semester-option]");

    if (!semesterOptions.length) {
      return;
    }

    semesterOptions.forEach((option) => {
      const input = option.querySelector('input[type="radio"]');

      if (!input) {
        return;
      }

      /*
       * Đồng bộ trạng thái ban đầu
       */
      option.classList.toggle("is-active", input.checked);

      option.addEventListener("click", () => {
        input.checked = true;

        semesterOptions.forEach((item) => {
          item.classList.remove("is-active");
        });

        option.classList.add("is-active");
      });
    });
  }

  /* =========================================================
       UPDATE RULE NUMBERS
    ========================================================= */

  function updateRuleNumbers(type) {
    const rules = getRules(type);

    rules.forEach((rule, index) => {
      const number = rule.querySelector(".subject-rule-card__number");

      if (number) {
        number.textContent = String(index + 1).padStart(2, "0");
      }

      const title = rule.querySelector(".subject-rule-card__header strong");

      if (title) {
        title.textContent = `Quy tắc số ${index + 1}`;
      }
    });

    /*
     * Badge số rule ở header
     */

    const countElement = form.querySelector(`[data-rule-count="${type}"]`);

    if (countElement) {
      countElement.textContent = rules.length;
    }

    /*
     * Summary
     */

    const summaryElement = form.querySelector(`[data-summary-count="${type}"]`);

    if (summaryElement) {
      summaryElement.textContent = `${rules.length} quy tắc`;
    }

    updateTotalRuleCount();
  }

  /* =========================================================
       UPDATE TOTAL RULE COUNT
    ========================================================= */

  function updateTotalRuleCount() {
    const theoryCount = getRuleCount("theory");

    const practiceCount = getRuleCount("practice");

    const total = theoryCount + practiceCount;

    const totalElement = form.querySelector('[data-summary-count="total"]');

    if (totalElement) {
      totalElement.textContent = `${total} quy tắc`;
    }
  }

  /* =========================================================
       CREATE RULE
    ========================================================= */

  function createRule(type, index) {
    const lessonTypeName = type === "theory" ? "Lý thuyết" : "Thực hành";

    const rule = document.createElement("div");

    rule.className = "subject-rule-card";

    rule.setAttribute("data-rule-item", "");

    rule.innerHTML = `

            <input
                type="hidden"
                name="rules[${type}][${index}][lesson_type]"
                value="${type}"
            >


            <div class="subject-rule-card__number">
                01
            </div>


            <div class="subject-rule-card__content">


                <!-- HEADER -->

                <div class="subject-rule-card__header">

                    <div>

                        <strong>
                            Quy tắc số 1
                        </strong>

                        <span>
                            ${lessonTypeName} · xác định khoảng tín chỉ.
                        </span>

                    </div>


                    <button
                        type="button"
                        class="subject-rule-remove"
                        data-remove-rule
                        title="Xóa quy tắc"
                    >

                        <i class="fa-light fa-trash-can"></i>

                    </button>

                </div>


                <!-- FIELDS -->

                <div class="subject-rule-fields">


                    <!-- MIN CREDIT -->

                    <div class="subject-rule-field">

                        <label>
                            Từ tín chỉ
                        </label>


                        <div class="subject-rule-input-wrapper">

                            <i class="fa-light fa-arrow-down-1-9"></i>


                            <input
                                type="number"
                                name="rules[${type}][${index}][min_credits]"
                                min="0"
                                placeholder="Không giới hạn"
                            >

                        </div>

                    </div>


                    <!-- MAX CREDIT -->

                    <div class="subject-rule-field">

                        <label>
                            Đến tín chỉ
                        </label>


                        <div class="subject-rule-input-wrapper">

                            <i class="fa-light fa-arrow-up-1-9"></i>


                            <input
                                type="number"
                                name="rules[${type}][${index}][max_credits]"
                                min="0"
                                placeholder="Không giới hạn"
                            >

                        </div>

                    </div>


                    <!-- TOTAL LESSONS -->

                    <div class="subject-rule-field subject-rule-field--lessons">

                        <label>

                            Tổng số buổi

                            <span class="required">
                                *
                            </span>

                        </label>


                        <div class="subject-rule-input-wrapper">

                            <i class="fa-light fa-list-ol"></i>


                            <input
                                type="number"
                                name="rules[${type}][${index}][total_lessons]"
                                min="1"
                                max="100"
                                placeholder="10"
                                required
                            >


                            <span>
                                buổi
                            </span>

                        </div>

                    </div>

                </div>


                <!-- EXAMPLE -->

                <div class="subject-rule-example">

                    <i class="fa-light fa-circle-info"></i>

                    <span>
                        Có thể để trống một đầu khoảng để biểu diễn
                        <strong>không giới hạn</strong>.
                    </span>

                </div>


            </div>
        `;

    return rule;
  }

  /* =========================================================
       ADD RULE
    ========================================================= */

  function initAddRule() {
    const addButtons = form.querySelectorAll("[data-add-rule]");

    addButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const type = button.dataset.addRule;

        if (type !== "theory" && type !== "practice") {
          return;
        }

        const list = getRuleList(type);

        if (!list) {
          return;
        }

        const index = ruleIndexes[type];

        const rule = createRule(type, index);

        list.appendChild(rule);

        ruleIndexes[type]++;

        updateRuleNumbers(type);

        /*
         * Focus vào input Từ tín chỉ
         * của rule mới
         */

        const firstInput = rule.querySelector('input[type="number"]');

        if (firstInput) {
          firstInput.focus();
        }
      });
    });
  }

  /* =========================================================
       REMOVE RULE
    ========================================================= */

  function initRemoveRule() {
    form.addEventListener("click", (event) => {
      const removeButton = event.target.closest("[data-remove-rule]");

      if (!removeButton) {
        return;
      }

      const rule = removeButton.closest("[data-rule-item]");

      if (!rule) {
        return;
      }

      const list = rule.closest("[data-rule-list]");

      if (!list) {
        return;
      }

      const type = list.dataset.ruleList;

      const rules = list.querySelectorAll("[data-rule-item]");

      /*
       * Luôn phải có ít nhất
       * một rule cho mỗi loại.
       */

      if (rules.length <= 1) {
        return;
      }

      rule.remove();

      updateRuleNumbers(type);
    });
  }

  /* =========================================================
       VALIDATE RULE
    ========================================================= */

  function validateRule(rule) {
    const minInput = rule.querySelector('input[name*="[min_credits]"]');

    const maxInput = rule.querySelector('input[name*="[max_credits]"]');

    const lessonsInput = rule.querySelector('input[name*="[total_lessons]"]');

    if (!lessonsInput) {
      return false;
    }

    /*
     * Tổng số buổi bắt buộc
     */

    const lessons = Number(lessonsInput.value);

    if (!lessons || lessons < 1 || lessons > 100) {
      lessonsInput.focus();

      return false;
    }

    /*
     * Từ tín chỉ
     */

    const minValue = minInput?.value.trim();

    /*
     * Đến tín chỉ
     */

    const maxValue = maxInput?.value.trim();

    /*
     * Nếu cả hai cùng có giá trị
     * thì min không được lớn hơn max.
     */

    if (minValue !== "" && maxValue !== "") {
      const min = Number(minValue);

      const max = Number(maxValue);

      if (min > max) {
        maxInput.focus();

        return false;
      }
    }

    return true;
  }

  /* =========================================================
       VALIDATE RULE OVERLAP
    ========================================================= */

  function validateRuleOverlaps(type) {
    const rules = getRules(type);

    const ranges = [];

    for (const rule of rules) {
      const minInput = rule.querySelector('input[name*="[min_credits]"]');

      const maxInput = rule.querySelector('input[name*="[max_credits]"]');

      const min = minInput?.value.trim() !== "" ? Number(minInput.value) : null;

      const max = maxInput?.value.trim() !== "" ? Number(maxInput.value) : null;

      ranges.push({
        rule,
        min,
        max,
      });
    }

    /*
     * Kiểm tra hai khoảng có giao nhau không.
     *
     * Ví dụ:
     *
     * 1 - 2
     * 2 - 4
     *
     * => giao nhau tại 2
     */

    for (let i = 0; i < ranges.length; i++) {
      for (let j = i + 1; j < ranges.length; j++) {
        const first = ranges[i];

        const second = ranges[j];

        const firstMin = first.min ?? -Infinity;

        const firstMax = first.max ?? Infinity;

        const secondMin = second.min ?? -Infinity;

        const secondMax = second.max ?? Infinity;

        const overlap = firstMin <= secondMax && secondMin <= firstMax;

        if (overlap) {
          const input = second.rule.querySelector(
            'input[name*="[min_credits]"]',
          );

          if (input) {
            input.focus();
          }

          return false;
        }
      }
    }

    return true;
  }

  /* =========================================================
       VALIDATE FORM
    ========================================================= */

  function validateForm() {
    /*
     * Học kỳ
     */

    const semester = form.querySelector(
      'input[name="semester_number"]:checked',
    );

    if (!semester) {
      const firstSemester = form.querySelector("[data-semester-option]");

      if (firstSemester) {
        firstSemester.focus();
      }

      return false;
    }

    /*
     * Theory + Practice
     */

    const types = ["theory", "practice"];

    for (const type of types) {
      const rules = getRules(type);

      /*
       * Mỗi lesson type phải
       * có ít nhất một rule.
       */

      if (!rules.length) {
        return false;
      }

      /*
       * Validate từng rule
       */

      for (const rule of rules) {
        if (!validateRule(rule)) {
          return false;
        }
      }

      /*
       * Validate khoảng bị trùng
       */

      if (!validateRuleOverlaps(type)) {
        return false;
      }
    }

    return true;
  }

  /* =========================================================
       SUBMIT
    ========================================================= */

  function initSubmit() {
    form.addEventListener("submit", (event) => {
      const isValid = validateForm();

      if (!isValid) {
        event.preventDefault();

        return;
      }
    });
  }

  /* =========================================================
       INITIALIZE
    ========================================================= */

  initSemesterSelection();

  initAddRule();

  initRemoveRule();

  initSubmit();

  updateRuleNumbers("theory");

  updateRuleNumbers("practice");
}

/* =========================================================
   DOM READY
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  initSubjectLessonPlanRules();
});
