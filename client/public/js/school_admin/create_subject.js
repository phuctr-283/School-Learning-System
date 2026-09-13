document.addEventListener("DOMContentLoaded", () => {
    const processInput = document.getElementById("processPercent");
    const midtermInput = document.getElementById("midtermPercent");
    const finalInput = document.getElementById("finalPercent");

    const totalElement = document.getElementById("percentTotal");

    function updateTotal() {
        const process = parseFloat(processInput.value) || 0;
        const midterm = parseFloat(midtermInput.value) || 0;
        const final = parseFloat(finalInput.value) || 0;

        const total = process + midterm + final;

        totalElement.textContent = `${total}%`;

        totalElement.classList.toggle(
            "subject-percent-preview__total--valid",
            total === 100
        );
    }

    [processInput, midtermInput, finalInput].forEach((input) => {
        input.addEventListener("input", updateTotal);
    });

    updateTotal();
});