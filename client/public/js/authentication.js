document.addEventListener("DOMContentLoaded", () => {
  initAuthAlert();
  initAuthSwitch();
  initUniversityDepartmentSelect();
  initRegisterValidation();
});
function initAuthAlert() {
  const alert = document.querySelector(".auth-alert");
  const closeButton = document.querySelector(".auth-alert-close");
  if (!alert) return;
  let removeTimer;
  function closeAlert() {
    if (!alert) return;
    alert.classList.add("is-closing");
    removeTimer = setTimeout(() => {
      alert.remove();
    }, 300);
  }
  closeButton?.addEventListener("click", closeAlert);
  setTimeout(() => {
    if (document.body.contains(alert)) {
      closeAlert();
    }
  }, 5000);
}

function initAuthSwitch() {
  const authContainer = document.querySelector(".auth-container");
  if (
    !authContainer ||
    authContainer.classList.contains("auth-container-admin")
  )
    return;
  const toRegisterBtn = document.getElementById("toRegisterBtn");
  const toLoginBtn = document.getElementById("toLoginBtn");
  const toRegisterMobile = document.getElementById("toRegisterMobile");
  const toLoginMobile = document.getElementById("toLoginMobile");
  function showRegister() {
    authContainer.classList.add("show-register");
  }
  function showLogin() {
    authContainer.classList.remove("show-register");
  }
  toRegisterBtn?.addEventListener("click", showRegister);
  toLoginBtn?.addEventListener("click", showLogin);
  toRegisterMobile?.addEventListener("click", (event) => {
    event.preventDefault();
    showRegister();
  });

  toLoginMobile?.addEventListener("click", (event) => {
    event.preventDefault();
    showLogin();
  });
}

function initRegisterValidation() {
  const form = document.querySelector(".register-form");

  if (!form) {
    return;
  }

  const isAdminRegister = form.classList.contains("admin-register-form");
  const fullName = isAdminRegister
    ? document.getElementById("adminFullName")
    : document.getElementById("regFullName");

  const fullNameCheck = isAdminRegister
    ? document.getElementById("adminFullNameCheck")
    : null;
  const username = isAdminRegister
    ? document.getElementById("adminUsername")
    : document.getElementById("regEmail");

  const usernameCheck = isAdminRegister
    ? document.getElementById("adminEmailCheck")
    : document.getElementById("emailCheck");

  const usernameError = isAdminRegister
    ? document.getElementById("adminEmailError")
    : document.getElementById("regUsernameError");

  const password = isAdminRegister
    ? document.getElementById("adminPassword")
    : document.getElementById("regPassword");

  const passwordCheck = isAdminRegister
    ? document.getElementById("adminPasswordCheck")
    : document.getElementById("passwordCheck");

  const confirmPassword = isAdminRegister
    ? document.getElementById("adminConfirmPassword")
    : document.getElementById("regConfirmPassword");

  const confirmCheck = isAdminRegister
    ? document.getElementById("adminConfirmCheck")
    : document.getElementById("confirmCheck");

  const meterBars = isAdminRegister
    ? document.getElementById("adminMeterBars")
    : document.getElementById("meterBars");

  const strengthText = isAdminRegister
    ? document.getElementById("adminStrengthText")
    : document.getElementById("strengthText");

  if (!fullName || !username || !password || !confirmPassword) {
    console.error("REGISTER: Thiếu element cần thiết.");

    return;
  }

  function validateFullName() {
    const value = fullName.value.trim();

    const isValid = value.length > 0;

    if (fullNameCheck) {
      fullNameCheck.style.display = isValid ? "block" : "none";
    }

    return isValid;
  }
  fullName.addEventListener("input", validateFullName);
  fullName.addEventListener("blur", validateFullName);
  function validateUsername() {
    const value = username.value.trim().toLowerCase();

    let isValid = false;
    if (isAdminRegister) {
      const superAdminPattern = /^[^\s@]+@admin\.vn$/;
      const schoolAdminPattern = /^[^\s@]+@admin\.stu\.edu\.vn$/;
      isValid = superAdminPattern.test(value) || schoolAdminPattern.test(value);
    } else {
      const userPattern = /^[^\s@]+@stu\.edu\.vn$/;
      isValid = userPattern.test(value);
    }
    const inputGroup = username.closest(".input-group");
    const hint = inputGroup?.querySelector(".input-hint");
    if (hint) {
      hint.style.opacity =
        value.length === 0 && document.activeElement === username ? "1" : "0";
    }
    if (usernameCheck) {
      usernameCheck.style.display = isValid ? "block" : "none";
    }
    if (usernameError) {
      usernameError.textContent =
        isValid || value.length === 0
          ? ""
          : isAdminRegister
            ? "Username phải có dạng example@admin.vn hoặc example@admin.stu.edu.vn"
            : "Username phải có dạng example@stu.edu.vn";
    }

    return isValid;
  }
  username.addEventListener("input", validateUsername);
  username.addEventListener("focus", validateUsername);
  username.addEventListener("blur", validateUsername);
  function getPasswordStrength(value) {
    const hasLetters = /[a-zA-Z]/.test(value);
    const hasNumbers = /[0-9]/.test(value);
    const hasUppercase = /[A-Z]/.test(value);
    const hasSpecial = /[^a-zA-Z0-9]/.test(value);
    if (hasLetters && hasNumbers && hasUppercase && hasSpecial) {
      return "high";
    }
    if (hasLetters && hasNumbers && hasUppercase) {
      return "medium";
    }
    if (hasLetters && hasNumbers) {
      return "low";
    }
    return "weak";
  }
  function updatePasswordMeter() {
    const value = password.value;
    if (!meterBars || !strengthText) {
      return false;
    }
    meterBars.className = "meter-bar-wrapper";
    if (!value.length) {
      strengthText.textContent = "Chưa nhập";
      strengthText.style.color = "#64748b";
      if (passwordCheck) {
        passwordCheck.style.display = "none";
      }
      updateConfirmPassword();
      return false;
    }
    const strength = getPasswordStrength(value);
    switch (strength) {
      case "low":
        meterBars.classList.add("low");
        strengthText.textContent = "Yếu";
        strengthText.style.color = "#ef4444";
        break;
      case "medium":
        meterBars.classList.add("medium");
        strengthText.textContent = "Trung bình";
        strengthText.style.color = "#f97316";
        break;
      case "high":
        meterBars.classList.add("high");
        strengthText.textContent = "Mạnh";
        strengthText.style.color = "#22c55e";
        break;
      default:
        meterBars.classList.add("low");
        strengthText.textContent = "Yếu";
        strengthText.style.color = "#ef4444";
    }
    const isLengthValid = value.length >= 8 && value.length <= 20;
    const isStrengthValid = strength === "medium" || strength === "high";
    console.log("PASSWORD DEBUG:", {
      length: value.length,
      strength: strength,
      isLengthValid: isLengthValid,
      isStrengthValid: isStrengthValid,
    });
    const isValid = isLengthValid && isStrengthValid;
    if (passwordCheck) {
      passwordCheck.style.display = isValid ? "block" : "none";
    }
    updateConfirmPassword();
    return isValid;
  }
  password.addEventListener("input", updatePasswordMeter);
  function updateConfirmPassword() {
    const passwordValue = password.value;
    const confirmValue = confirmPassword.value;
    const isValid = confirmValue.length > 0 && confirmValue === passwordValue;
    if (confirmCheck) {
      confirmCheck.style.display = isValid ? "block" : "none";
    }
    return isValid;
  }
  confirmPassword.addEventListener("input", updateConfirmPassword);
  form.addEventListener("submit", function (event) {
    const isFullNameValid = validateFullName();
    const isUsernameValid = validateUsername();
    const isPasswordValid = updatePasswordMeter();
    const isConfirmValid = updateConfirmPassword();

    // ==========================================
    // ADMIN REGISTER
    // ==========================================

    if (isAdminRegister) {
      console.log("ADMIN REGISTER VALIDATION:", {
        fullName: isFullNameValid,
        username: isUsernameValid,
        password: isPasswordValid,
        confirmPassword: isConfirmValid,
      });

      if (
        !isFullNameValid ||
        !isUsernameValid ||
        !isPasswordValid ||
        !isConfirmValid
      ) {
        event.preventDefault();

        console.log("ADMIN REGISTER: Validation failed");

        return;
      }

      console.log("ADMIN REGISTER: Validation passed");

      return;
    }

    // ==========================================
    // TEACHER REGISTER
    // ==========================================

    const university = document.getElementById("regUniversity");

    const department = document.getElementById("regDepartment");

    const isUniversityValid = university && university.value.trim().length > 0;

    const isDepartmentValid = department && department.value.trim().length > 0;

    console.log("TEACHER REGISTER VALIDATION:", {
      fullName: isFullNameValid,
      username: isUsernameValid,
      university: isUniversityValid,
      department: isDepartmentValid,
      password: isPasswordValid,
      confirmPassword: isConfirmValid,
    });

    if (
      !isFullNameValid ||
      !isUsernameValid ||
      !isUniversityValid ||
      !isDepartmentValid ||
      !isPasswordValid ||
      !isConfirmValid
    ) {
      event.preventDefault();

      console.log("REGISTER: Validation failed");

      return;
    }

    console.log("REGISTER: Validation passed - submitting form");

    // Không gọi preventDefault()
    // => trình duyệt POST /register
  });
}
function initUniversityDepartmentSelect() {
  const universitySelect = document.getElementById("regUniversity");

  const departmentSelect = document.getElementById("regDepartment");

  if (!universitySelect || !departmentSelect) {
    return;
  }

  departmentSelect.disabled = true;

  departmentSelect.innerHTML = `
    <option value="" disabled selected>
      -- Chọn trường trước --
    </option>
  `;

  universitySelect.addEventListener("change", async function () {
    const universityId = this.value.trim();

    departmentSelect.disabled = true;

    departmentSelect.innerHTML = `
        <option value="" disabled selected>
          Đang tải danh sách khoa...
        </option>
      `;

    if (!universityId) {
      departmentSelect.innerHTML = `
          <option value="" disabled selected>
            -- Chọn trường trước --
          </option>
        `;

      return;
    }

    try {
      const response = await fetch(
        `/register/departments?university_id=${encodeURIComponent(
          universityId,
        )}`,
        {
          method: "GET",

          headers: {
            Accept: "application/json",
          },
        },
      );
      const result = await response.json();
      if (!response.ok || !result.success) {
        throw new Error(result.message || "Không thể lấy danh sách khoa");
      }
      if (!Array.isArray(result.data) || result.data.length === 0) {
        departmentSelect.innerHTML = `
            <option value="" disabled selected>
              -- Chưa có khoa --
            </option>
          `;
        departmentSelect.disabled = true;
        return;
      }
      departmentSelect.innerHTML = `
          <option value="" disabled selected>
            -- Chọn khoa --
          </option>
        `;
      result.data.forEach((department) => {
        const option = document.createElement("option");
        option.value = department.departmentId;
        option.textContent = `${department.name}`;
        departmentSelect.appendChild(option);
      });
      departmentSelect.disabled = false;
    } catch (error) {
      console.error("GET DEPARTMENTS ERROR:", error);
      departmentSelect.innerHTML = `
          <option value="" disabled selected>
            -- Không thể tải danh sách khoa --
          </option>
        `;
      departmentSelect.disabled = true;
    }
  });
}
