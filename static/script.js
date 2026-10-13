// ===============================
// DOM ELEMENTS
// ===============================
const form = document.getElementById("predictionForm");
const riskValue = document.getElementById("riskValue");
const riskBadge = document.getElementById("riskBadge");
const driverList = document.getElementById("driverList");
const populationComparison = document.getElementById("populationComparison");
const downloadBtn = document.getElementById("downloadReport");
const recommendationText = document.getElementById("recommendationText");


// ===============================
// EVENT LISTENER
// ===============================
form.addEventListener("submit", handlePrediction);


// ===============================
// MAIN PREDICTION FUNCTION
// ===============================
function handlePrediction(e) {
    e.preventDefault();

    const data = collectFormData();

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(response => {
        updateUI(response);
    })
    .catch(() => {
        riskValue.innerText = "Server error. Try again.";
    });
}


// ===============================
// COLLECT FORM DATA
// ===============================
function collectFormData() {
    return {
        Age: Number(age.value),
        Height: Number(height.value),
        Weight: Number(weight.value),
        SleepHours: Number(sleep.value),
        StressLevel: Number(stress.value),
        BMI: Number(bmi.value),
        Gender: gender.value,
        Occupation: occupation.value,
        Diet: diet.value,
        JunkFood: junkfood.value,
        Smoking: smoking.value,
        Alcohol: alcohol.value,
        FamilyHistory: family.value
    };
}


// ===============================
// UPDATE UI WITH RESPONSE
// ===============================
function updateUI(response) {

    const risk = response.risk;

    // Risk Value
    riskValue.innerText = `Predicted Risk: ${risk}%`;

    // Badge
    riskBadge.innerText = response.category;
    riskBadge.className = "badge " + response.category.toLowerCase();

    // Drivers
    driverList.innerHTML = "";
    response.drivers.forEach(driver => {
        const li = document.createElement("li");
        li.innerText = driver;
        driverList.appendChild(li);
    });

    // Population comparison
    populationComparison.innerText = response.population_comparison;

    // Recommendation
    generateRecommendation(risk);

    // Enable PDF download
    downloadBtn.style.display = "block";
    downloadBtn.onclick = () => {
        window.open(`http://127.0.0.1:5000/report/${response.prediction_id}`);
    };
}


// ===============================
// RECOMMENDATION LOGIC
// ===============================
function generateRecommendation(risk) {
    let recommendation = "";

    if (risk < 30) {
        recommendation = "Maintain your current lifestyle. Continue healthy habits.";
    }
    else if (risk < 60) {
        recommendation = "Moderate risk detected. Improve sleep, diet, and stress management.";
    }
    else {
        recommendation = "High risk detected. Immediate lifestyle modification and medical consultation recommended.";
    }

    recommendationText.innerText = recommendation;
}
