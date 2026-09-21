document.addEventListener("DOMContentLoaded", () => {
  const DESKTOP_BREAKPOINT = 992;
  const SIDEBAR_STORAGE_KEY = "school-learning-sidebar-state";

  const sidebar = document.getElementById("sidebar");

  const sidebarMenu = document.querySelector(".sidebar-menu");

  const menuToggle = document.getElementById("menuToggle");

  const overlay = document.getElementById("overlay");

  const closeSidebar = document.getElementById("closeSidebar");

  const userProfileBtn = document.getElementById("userProfileBtn");

  const userProfileWrapper = document.querySelector(".user-profile-wrapper");

  if (sidebar && sidebarMenu) {
    initializeSidebar();
  }

  if (userProfileBtn && userProfileWrapper) {
    initializeUserProfile();
  }

  function initializeSidebar() {
    restoreSidebarState();

    document.documentElement.classList.remove("sidebar-precollapsed");

    const activeItem = findActiveMenuItem();

    applyActiveMenu(activeItem);

    const activeIndicator = createActiveIndicator();

    if (activeIndicator && activeItem) {
      moveActiveIndicator(activeIndicator, activeItem, false);
    }

    updateMenuIcon();

    if (menuToggle) {
      menuToggle.addEventListener("click", handleMenuToggle);
    }

    if (overlay) {
      overlay.addEventListener("click", closeMobileSidebar);
    }

    if (closeSidebar) {
      closeSidebar.addEventListener("click", closeMobileSidebar);
    }

    initializeMenuClick(activeIndicator);

    window.addEventListener("resize", () => {
      handleSidebarResize(activeIndicator);
    });
  }

  function restoreSidebarState() {
    const isDesktop = window.innerWidth >= DESKTOP_BREAKPOINT;

    if (!isDesktop) {
      sidebar.classList.remove("collapsed");

      sidebar.classList.remove("show");

      if (overlay) {
        overlay.classList.remove("show");
      }

      return;
    }

    let savedState = null;

    try {
      savedState = localStorage.getItem(SIDEBAR_STORAGE_KEY);
    } catch (error) {
      savedState = null;
    }

    if (savedState === "collapsed") {
      sidebar.classList.add("collapsed");
    } else {
      sidebar.classList.remove("collapsed");
    }
  }

  function saveSidebarState() {
    const isCollapsed = sidebar.classList.contains("collapsed");

    try {
      localStorage.setItem(
        SIDEBAR_STORAGE_KEY,
        isCollapsed ? "collapsed" : "expanded",
      );
    } catch (error) {}
  }

  function updateMenuIcon() {
    if (!menuToggle) {
      return;
    }

    const isDesktop = window.innerWidth >= DESKTOP_BREAKPOINT;

    const isCollapsed = sidebar.classList.contains("collapsed");

    if (isDesktop) {
      menuToggle.classList.remove("is-mobile");

      menuToggle.classList.toggle("is-collapsed", isCollapsed);
    } else {
      menuToggle.classList.remove("is-collapsed");

      menuToggle.classList.add("is-mobile");
    }
  }

  function handleMenuToggle() {
    const isDesktop = window.innerWidth >= DESKTOP_BREAKPOINT;

    if (isDesktop) {
      sidebar.classList.toggle("collapsed");

      saveSidebarState();

      updateMenuIcon();

      return;
    }

    sidebar.classList.toggle("show");

    if (overlay) {
      overlay.classList.toggle("show");
    }
  }

  function closeMobileSidebar() {
    sidebar.classList.remove("show");

    if (overlay) {
      overlay.classList.remove("show");
    }
  }

  function handleSidebarResize(activeIndicator) {
    const isDesktop = window.innerWidth >= DESKTOP_BREAKPOINT;

    if (isDesktop) {
      sidebar.classList.remove("show");

      if (overlay) {
        overlay.classList.remove("show");
      }

      restoreSidebarState();
    } else {
      sidebar.classList.remove("collapsed");

      sidebar.classList.remove("show");

      if (overlay) {
        overlay.classList.remove("show");
      }
    }

    updateMenuIcon();

    if (activeIndicator) {
      const currentActive = sidebarMenu.querySelector(
        ":scope > li.side-active",
      );

      if (currentActive) {
        moveActiveIndicator(activeIndicator, currentActive, false);
      }
    }
  }

  function findActiveMenuItem() {
    const currentPath = normalizePath(window.location.pathname);

    const menuItems = sidebarMenu.querySelectorAll(":scope > li");

    let activeItem = null;
    let longestMatch = 0;

    menuItems.forEach((item) => {
      const link = item.querySelector(":scope > a");

      if (!link) {
        return;
      }

      const href = link.getAttribute("href");

      if (!href || href === "#" || href.startsWith("javascript:")) {
        return;
      }

      let linkUrl;

      try {
        linkUrl = new URL(href, window.location.origin);
      } catch (error) {
        return;
      }

      if (linkUrl.origin !== window.location.origin) {
        return;
      }

      const linkPath = normalizePath(linkUrl.pathname);

      const isRoleHome = isRoleHomePath(linkPath);

      let isMatch = false;

      if (isRoleHome) {
        isMatch = currentPath === linkPath;
      } else {
        isMatch =
          currentPath === linkPath || currentPath.startsWith(`${linkPath}/`);
      }

      if (isMatch && linkPath.length > longestMatch) {
        activeItem = item;
        longestMatch = linkPath.length;
      }
    });

    return activeItem;
  }

  function isRoleHomePath(path) {
    return (
      path === "/super-admin" ||
      path === "/school-admin" ||
      path === "/teacher" ||
      path === "/student"
    );
  }

  function normalizePath(path) {
    if (!path) {
      return "/";
    }

    const normalized = path.replace(/\/+$/, "");

    return normalized || "/";
  }

  function applyActiveMenu(activeItem) {
    const menuItems = sidebarMenu.querySelectorAll(":scope > li");

    menuItems.forEach((item) => {
      item.classList.remove("side-active");
    });

    if (activeItem) {
      activeItem.classList.add("side-active");
    }
  }

  function createActiveIndicator() {
    let indicator = sidebarMenu.querySelector(
      ":scope > .sidebar-active-indicator",
    );

    if (indicator) {
      return indicator;
    }

    indicator = document.createElement("div");

    indicator.className = "sidebar-active-indicator";

    sidebarMenu.prepend(indicator);

    return indicator;
  }

  function moveActiveIndicator(indicator, item, animate = true) {
    if (!indicator || !item) {
      return;
    }

    const menuRect = sidebarMenu.getBoundingClientRect();

    const itemRect = item.getBoundingClientRect();

    const top = itemRect.top - menuRect.top;

    if (!animate) {
      indicator.style.transition = "none";
    }

    indicator.style.top = `${top}px`;

    if (!animate) {
      indicator.offsetHeight;

      indicator.style.transition = "";
    }

    indicator.style.display = "block";
  }

  function initializeMenuClick(indicator) {
    const menuItems = sidebarMenu.querySelectorAll(":scope > li");

    menuItems.forEach((item) => {
      const link = item.querySelector(":scope > a");

      if (!link) {
        return;
      }

      link.addEventListener("click", () => {
        const href = link.getAttribute("href");

        if (!href || href === "#") {
          return;
        }

        menuItems.forEach((menuItem) => {
          menuItem.classList.remove("side-active");
        });

        item.classList.add("side-active");

        if (indicator) {
          indicator.style.display = "block";

          moveActiveIndicator(indicator, item, true);
        }

        if (window.innerWidth < DESKTOP_BREAKPOINT) {
          closeMobileSidebar();
        }
      });
    });
  }

  function initializeUserProfile() {
    userProfileBtn.addEventListener("click", (event) => {
      event.stopPropagation();

      userProfileWrapper.classList.toggle("active");
    });

    document.addEventListener("click", () => {
      userProfileWrapper.classList.remove("active");
    });

    userProfileWrapper.addEventListener("click", (event) => {
      event.stopPropagation();
    });
  }
});
