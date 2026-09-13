document.addEventListener("DOMContentLoaded", () => {
  initImportForms();
});

/* =========================================================
   IMPORT FORMS
========================================================= */

function initImportForms() {
  const forms = document.querySelectorAll(".import-form");

  forms.forEach((form) => {
    initImportForm(form);
  });
}

/* =========================================================
   INIT IMPORT FORM
========================================================= */

function initImportForm(form) {
  const fileInput = form.querySelector('input[type="file"]');

  if (!fileInput) {
    return;
  }

  const fileName = form.querySelector(".import-upload__filename");

  const filePreview = form.querySelector(".import-file-preview");

  const previewName = form.querySelector(".import-file-preview__name");

  const previewSize = form.querySelector(".import-file-preview__size");

  const removeFile = form.querySelector(".import-file-preview__remove");

  const importButton = form.querySelector(".import-btn");

  const normalButton = importButton?.querySelector(".import-btn__normal");

  const loadingButton = importButton?.querySelector(".import-btn__loading");

  /* =====================================================
     FILE CHANGE
  ===================================================== */

  fileInput.addEventListener("change", () => {
    const file = fileInput.files?.[0];

    if (!file) {
      resetImportFile();

      return;
    }

    /* =================================================
       VALIDATE EXTENSION
    ================================================= */

    const validation = validateImportFile(file, fileInput);

    if (!validation.valid) {
      alert(validation.message);

      resetImportFile();

      return;
    }

    /* =================================================
       VALIDATE FILE SIZE
    ================================================= */

    const maxSize = 128 * 1024 * 1024;

    if (file.size > maxSize) {
      alert("Dung lượng tập tin không được vượt quá 128 MiB.");

      resetImportFile();

      return;
    }

    /* =================================================
       FILE NAME
    ================================================= */

    if (fileName) {
      fileName.textContent = file.name;

      fileName.classList.add("has-file");
    }

    /* =================================================
       PREVIEW NAME
    ================================================= */

    if (previewName) {
      previewName.textContent = file.name;
    }

    /* =================================================
       PREVIEW SIZE
    ================================================= */

    if (previewSize) {
      previewSize.textContent = formatFileSize(file.size);
    }

    /* =================================================
       SHOW PREVIEW
    ================================================= */

    if (filePreview) {
      filePreview.hidden = false;
    }
  });

  /* =====================================================
     REMOVE FILE
  ====================================================== */

  removeFile?.addEventListener("click", resetImportFile);

  /* =====================================================
     FORM SUBMIT
  ====================================================== */

  form.addEventListener("submit", (event) => {
    if (!fileInput.files?.length) {
      event.preventDefault();

      return;
    }

    setImportLoading(true);
  });

  /* =====================================================
     RESET FILE
  ====================================================== */

  function resetImportFile() {
    fileInput.value = "";

    if (fileName) {
      fileName.textContent = "Chưa chọn tập tin";

      fileName.classList.remove("has-file");
    }

    if (filePreview) {
      filePreview.hidden = true;
    }

    if (previewName) {
      previewName.textContent = "-";
    }

    if (previewSize) {
      previewSize.textContent = "-";
    }
  }

  /* =====================================================
     LOADING
  ====================================================== */

  function setImportLoading(loading) {
    if (!importButton) {
      return;
    }

    importButton.disabled = loading;

    if (normalButton) {
      normalButton.hidden = loading;
    }

    if (loadingButton) {
      loadingButton.hidden = !loading;
    }
  }
}

/* =========================================================
   IMPORT RESULT
========================================================= */

document.addEventListener("click", (event) => {
  const closeButton = event.target.closest(".import-result__close");

  const resetButton = event.target.closest(".import-result__reset");

  /* =====================================================
     CLOSE RESULT
  ====================================================== */

  if (closeButton) {
    const result = closeButton.closest(".import-result");

    result?.remove();

    return;
  }

  /* =====================================================
     IMPORT AGAIN
  ====================================================== */

  if (resetButton) {
    const result = resetButton.closest(".import-result");

    const card = resetButton.closest(".import-card");

    const form = card?.querySelector(".import-form");

    result?.remove();

    if (!form) {
      return;
    }

    form.reset();

    resetImportFormUI(form);

    const formTop = form.getBoundingClientRect().top + window.scrollY;

    window.scrollTo({
      top: formTop - 30,
      behavior: "smooth",
    });
  }
});

/* =========================================================
   RESET IMPORT FORM UI
========================================================= */

function resetImportFormUI(form) {
  const fileName = form.querySelector(".import-upload__filename");

  const filePreview = form.querySelector(".import-file-preview");

  const previewName = form.querySelector(".import-file-preview__name");

  const previewSize = form.querySelector(".import-file-preview__size");

  const importButton = form.querySelector(".import-btn");

  const normalButton = importButton?.querySelector(".import-btn__normal");

  const loadingButton = importButton?.querySelector(".import-btn__loading");

  /* FILE NAME */

  if (fileName) {
    fileName.textContent = "Chưa chọn tập tin";

    fileName.classList.remove("has-file");
  }

  /* FILE PREVIEW */

  if (filePreview) {
    filePreview.hidden = true;
  }

  /* PREVIEW NAME */

  if (previewName) {
    previewName.textContent = "-";
  }

  /* PREVIEW SIZE */

  if (previewSize) {
    previewSize.textContent = "-";
  }

  /* BUTTON */

  if (importButton) {
    importButton.disabled = false;
  }

  if (normalButton) {
    normalButton.hidden = false;
  }

  if (loadingButton) {
    loadingButton.hidden = true;
  }
}

/* =========================================================
   VALIDATE FILE
========================================================= */

function validateImportFile(file, fileInput) {
  const fileName = file.name.toLowerCase();

  /* =====================================================
     GET ACCEPTED EXTENSIONS
  ====================================================== */

  const accept = fileInput.getAttribute("accept")?.trim();

  if (!accept) {
    return {
      valid: true,
      message: "",
    };
  }

  const acceptedExtensions = accept
    .split(",")
    .map((item) => item.trim().toLowerCase())
    .filter((item) => item.startsWith("."));

  if (!acceptedExtensions.length) {
    return {
      valid: true,
      message: "",
    };
  }

  /* =====================================================
     CHECK EXTENSION
  ====================================================== */

  const isValid = acceptedExtensions.some((extension) =>
    fileName.endsWith(extension),
  );

  if (isValid) {
    return {
      valid: true,
      message: "",
    };
  }

  /* =====================================================
     ERROR MESSAGE
  ====================================================== */

  return {
    valid: false,

    message:
      "Định dạng tập tin không được hỗ trợ. " +
      "Chỉ chấp nhận: " +
      acceptedExtensions.join(", ").toUpperCase(),
  };
}

/* =========================================================
   FORMAT FILE SIZE
========================================================= */

function formatFileSize(bytes) {
  if (!bytes) {
    return "0 KB";
  }

  const units = ["B", "KB", "MB", "GB"];

  const index = Math.min(
    Math.floor(Math.log(bytes) / Math.log(1024)),
    units.length - 1,
  );

  const size = bytes / Math.pow(1024, index);

  return size.toFixed(index === 0 ? 0 : 2) + " " + units[index];
}
