document.addEventListener("DOMContentLoaded", () => {
  initLessonPanels();
});

/* =========================================================
   INIT LESSON PANELS
========================================================= */

function initLessonPanels() {
  const sidebarItems = document.querySelectorAll(".lesson-sidebar-item");

  const panels = document.querySelectorAll(".lesson-panel");

  if (!sidebarItems.length || !panels.length) {
    return;
  }

  sidebarItems.forEach((item) => {
    item.addEventListener("click", () => {
      const target = item.dataset.target;

      if (!target) {
        return;
      }

      setActiveSidebarItem(sidebarItems, item);

      setActiveLessonPanel(panels, target);
    });
  });
}

/* =========================================================
   SET ACTIVE SIDEBAR ITEM
========================================================= */

function setActiveSidebarItem(sidebarItems, activeItem) {
  sidebarItems.forEach((item) => {
    item.classList.remove("is-active");
  });

  activeItem.classList.add("is-active");
}

/* =========================================================
   SET ACTIVE LESSON PANEL
========================================================= */

function setActiveLessonPanel(panels, target) {
  panels.forEach((panel) => {
    const isActive = panel.dataset.panel === target;

    panel.classList.toggle("is-active", isActive);
  });
}
