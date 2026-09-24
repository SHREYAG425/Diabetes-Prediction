// ---- 1. Gender toggle buttons ----
// Clicking a button marks it "active" and un-marks the others.
const genderButtons = document.querySelectorAll('[data-field="gender"] .toggle-btn');
let selectedGender = "Female"; // default, matches the button marked "active" in HTML

genderButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    genderButtons.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    selectedGender = btn.dataset.value;
  });
});


// ---- 2. Live labels next to the sliders ----
// Every time a slider moves, update the little number badge next to its label.
function linkSliderToLabel(sliderId, labelId) {
  const slider = document.getElementById(sliderId);
  const label = document.getElementById(labelId);
  label.textContent = slider.value;
  slider.addEventListener("input", () => {
    label.textContent = slider.value;
  });
}

linkSliderToLabel("age", "age-value");
linkSliderToLabel("bmi", "bmi-value");
linkSliderToLabel("HbA1c_level", "hba1c-value");
linkSliderToLabel("blood_glucose_level", "glucose-value");


// ---- 3. Form submission (AJAX — no page reload) ----
const form = document.getElementById("predict-form");
const submitBtn = document.getElementById("submit-btn");
const submitText = document.getElementById("submit-text");

const resultEmpty = document.getElementById("result-empty");
const resultContent = document.getElementById("result-content");
const resultLabel = document.getElementById("result-label");
const barFill = document.getElementById("probability-bar-fill");
const probabilityText = document.getElementById("probability-text");

form.addEventListener("submit", async (event) => {
  event.preventDefault(); // stop the browser from reloading the page

  // Collect all the input values into one object.
  const payload = {
    gender: selectedGender,
    age: document.getElementById("age").value,
    hypertension: document.getElementById("hypertension").checked ? 1 : 0,
    heart_disease: document.getElementById("heart_disease").checked ? 1 : 0,
    smoking_history: document.getElementById("smoking_history").value,
    bmi: document.getElementById("bmi").value,
    HbA1c_level: document.getElementById("HbA1c_level").value,
    blood_glucose_level: document.getElementById("blood_glucose_level").value,
  };

  // Show a loading state on the button.
  submitBtn.disabled = true;
  submitText.textContent = "Checking...";

  try {
    // Send the data to Flask's /predict route as JSON.
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const result = await response.json();

    // Update the result panel with what the model predicted.
    resultEmpty.hidden = true;
    resultContent.hidden = false;

    resultLabel.textContent = result.label;
    resultLabel.className = "result-label " + (result.prediction === 1 ? "positive" : "negative");

    barFill.style.width = result.probability + "%";
    barFill.className = "probability-bar-fill " + (result.prediction === 1 ? "positive" : "");

    probabilityText.textContent = "Estimated probability: " + result.probability + "%";
  } catch (error) {
    resultEmpty.hidden = false;
    resultContent.hidden = true;
    alert("Something went wrong — please try again.");
    console.error(error);
  }

  submitBtn.disabled = false;
  submitText.textContent = "Check my risk";
});