document.addEventListener("DOMContentLoaded", () => {
  const root = document.querySelector("[data-history-root]");

  if (!root) {
    return;
  }

  const toggle = root.querySelector("[data-history-filter-toggle]");

  const buttonText = root.querySelector("[data-history-filter-button]");

  const buttonIcon = root.querySelector("[data-history-filter-icon]");

  const label = root.querySelector("[data-history-filter-label]");

  const modes = [
    {
      key: "correct",

      label: "Đáp án đúng",

      icon: "fa-circle-check",
    },

    {
      key: "wrong",

      label: "Đáp án sai",

      icon: "fa-circle-xmark",
    },

    {
      key: "all",

      label: "Hiển thị tất cả",

      icon: "fa-layer-group",
    },
  ];

  let currentIndex = 0;

  function applyFilter() {
    const mode = modes[currentIndex];

    if (buttonText) {
      buttonText.textContent = mode.label;
    }

    if (label) {
      label.textContent = mode.label;
    }

    if (buttonIcon) {
      buttonIcon.className = `fa-light ${mode.icon}`;
    }

    const options = root.querySelectorAll("[data-option]");

    options.forEach((option) => {
      const isCorrect = option.dataset.correct === "true";

      if (mode.key === "correct") {
        option.hidden = !isCorrect;
      } else if (mode.key === "wrong") {
        option.hidden = isCorrect;
      } else {
        option.hidden = false;
      }
    });
  }

  if (toggle) {
    toggle.addEventListener("click", () => {
      currentIndex = (currentIndex + 1) % modes.length;

      applyFilter();
    });
  }

  applyFilter();
});
