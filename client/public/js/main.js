document.addEventListener("DOMContentLoaded", () => {

    const currentPath =
        window.location.pathname
            .replace(/\/+$/, "") || "/";


    const menuItems =
        document.querySelectorAll(
            ".sidebar-menu > li"
        );


    let activeItem =
        null;

    let longestMatch =
        0;


    menuItems.forEach((item) => {

        const link =
            item.querySelector(":scope > a");

        if (!link) {
            return;
        }


        const href =
            link.getAttribute("href");

        if (
            !href ||
            href === "#"
        ) {
            return;
        }


        const linkPath =
            new URL(
                href,
                window.location.origin
            ).pathname
                .replace(/\/+$/, "") || "/";


        let isMatch =
            false;


        /*
        =========================================
        HOME PAGE
        =========================================
        */

        if (
            linkPath === "/admin" ||
            linkPath === "/teacher" ||
            linkPath === "/student"
        ) {

            isMatch =
                currentPath === linkPath;

        }


        /*
        =========================================
        EXACT / PARENT-CHILD
        =========================================
        */

        else if (
            currentPath === linkPath ||
            currentPath.startsWith(
                linkPath + "/"
            )
        ) {

            isMatch =
                true;

        }


        /*
        =========================================
        SAME ROLE + CATEGORY

        /student/assignment/lesson
        /student/assignment/assignment

        /teacher/assignment/subject
        /teacher/assignment/group
        =========================================
        */

        else {

            const linkParts =
                linkPath.split("/");

            const currentParts =
                currentPath.split("/");


            const linkRole =
                linkParts[1];

            const currentRole =
                currentParts[1];


            const linkCategory =
                linkParts[2];

            const currentCategory =
                currentParts[2];


            if (
                linkRole &&
                currentRole &&
                linkCategory &&
                currentCategory
            ) {

                isMatch =
                    linkRole === currentRole &&
                    linkCategory === currentCategory;

            }

        }


        /*
        =========================================
        LONGEST MATCH
        =========================================
        */

        if (
            isMatch &&
            linkPath.length > longestMatch
        ) {

            activeItem =
                item;

            longestMatch =
                linkPath.length;

        }

    });


    menuItems.forEach((item) => {

        item.classList.remove(
            "side-active"
        );

    });


    if (activeItem) {

        activeItem.classList.add(
            "side-active"
        );

    }

});
document.addEventListener("DOMContentLoaded", () => {
  const sidebarMenu = document.querySelector(".sidebar-menu");

  if (!sidebarMenu) return;

  const menuItems = sidebarMenu.querySelectorAll(":scope > li");

  if (!menuItems.length) return;

  /*
    =========================================
    CREATE ACTIVE INDICATOR
    =========================================
    */

  const activeIndicator = document.createElement("div");

  activeIndicator.className = "sidebar-active-indicator";

  sidebarMenu.prepend(activeIndicator);

  /*
    =========================================
    MOVE INDICATOR
    =========================================
    */

  function moveActiveIndicator(item, animate = true) {
    if (!item) return;

    const menuRect = sidebarMenu.getBoundingClientRect();
    const itemRect = item.getBoundingClientRect();

    const top = itemRect.top - menuRect.top;

    if (!animate) {
      activeIndicator.style.transition = "none";
    }

    activeIndicator.style.top = `${top}px`;

    if (!animate) {
      // Force browser repaint
      activeIndicator.offsetHeight;

      activeIndicator.style.transition = "";
    }
  }

  /*
    =========================================
    FIND ACTIVE ITEM
    =========================================
    */

  let activeItem = sidebarMenu.querySelector(":scope > li.side-active");

  /*
    =========================================
    INITIAL POSITION
    =========================================
    */

  if (activeItem) {
    moveActiveIndicator(activeItem, false);
  } else {
    activeIndicator.style.display = "none";
  }

  /*
    =========================================
    CLICK MENU
    =========================================
    */

  menuItems.forEach((item) => {
    const link = item.querySelector(":scope > a");

    if (!link) return;

    link.addEventListener("click", () => {
      if (link.getAttribute("href") === "#") {
        return;
      }

      menuItems.forEach((menuItem) => {
        menuItem.classList.remove("side-active");
      });

      item.classList.add("side-active");

      activeIndicator.style.display = "block";

      moveActiveIndicator(item, true);
    });
  });

  /*
    =========================================
    WINDOW RESIZE
    =========================================
    */

  window.addEventListener("resize", () => {
    const currentActive = sidebarMenu.querySelector(":scope > li.side-active");

    if (currentActive) {
      moveActiveIndicator(currentActive, false);
    }
  });
});
const userProfileBtn = document.getElementById("userProfileBtn");
const userProfileWrapper = document.querySelector(".user-profile-wrapper");

userProfileBtn.addEventListener("click", function (e) {
  e.stopPropagation();

  userProfileWrapper.classList.toggle("active");
});

document.addEventListener("click", function () {
  userProfileWrapper.classList.remove("active");
});
// ===================================================
// COLLAPSE + EXPAND SIDEBAR
// ===================================================

document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("sidebar");
  const menuToggle = document.getElementById("menuToggle");
  const overlay = document.getElementById("overlay");
  const closeSidebar = document.getElementById("closeSidebar");

  if (!sidebar || !menuToggle) return;

  // ===================================================
  // UPDATE MENU ICON
  // ===================================================

  function updateMenuIcon() {
    const isDesktop = window.innerWidth >= 992;
    const isCollapsed = sidebar.classList.contains("collapsed");

    if (isDesktop) {
      // Desktop
      menuToggle.classList.remove("is-mobile");

      // Sidebar collapsed -> expand icon
      // Sidebar normal    -> collapse icon
      menuToggle.classList.toggle("is-collapsed", isCollapsed);
    } else {
      // Mobile
      menuToggle.classList.remove("is-collapsed");
      menuToggle.classList.add("is-mobile");
    }
  }

  // ===================================================
  // INITIAL
  // ===================================================

  updateMenuIcon();

  // ===================================================
  // MENU TOGGLE
  // ===================================================

  menuToggle.addEventListener("click", () => {
    // ===============================
    // DESKTOP
    // ===============================

    if (window.innerWidth >= 992) {
      sidebar.classList.toggle("collapsed");

      updateMenuIcon();
    }

    // ===============================
    // MOBILE
    // ===============================
    else {
      sidebar.classList.toggle("show");

      overlay?.classList.toggle("show");
    }
  });

  // ===================================================
  // OVERLAY
  // ===================================================

  overlay?.addEventListener("click", () => {
    sidebar.classList.remove("show");

    overlay.classList.remove("show");
  });

  // ===================================================
  // CLOSE SIDEBAR
  // ===================================================

  closeSidebar?.addEventListener("click", () => {
    sidebar.classList.remove("show");

    overlay?.classList.remove("show");
  });

  // ===================================================
  // RESPONSIVE
  // ===================================================

  window.addEventListener("resize", () => {
    if (window.innerWidth >= 992) {
      // Xóa trạng thái mobile
      sidebar.classList.remove("show");

      overlay?.classList.remove("show");
    }

    updateMenuIcon();
  });
});
