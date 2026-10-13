// Protect page
if (sessionStorage.getItem("isAdmin") !== "true") {
    window.location.href = "/login";
}

function logout() {
    sessionStorage.removeItem("isAdmin");
    window.location.href = "/";
}

fetch("/analytics")
.then(res => res.json())
.then(data => {

    document.getElementById("totalUsers").innerText = data.total_users;
    document.getElementById("avgRisk").innerText = 
    data.average_risk ? data.average_risk.toFixed(2) + "%" : "0%";

    const dist = data.distribution;
const total = data.total_users;
const high = data.distribution.high;

let percent = 0;
if (total > 0) {
    percent = ((high / total) * 100).toFixed(1);
}

document.getElementById("highPercent").innerText = percent + "%";

    // Pie Chart
    new Chart(document.getElementById("pieChart"), {
        type: "pie",
        data: {
            labels: ["Low", "Moderate", "High"],
            datasets: [{
                data: [dist.low, dist.moderate, dist.high],
                backgroundColor: ["#22c55e", "#f59e0b", "#ef4444"]
            }]
        }
    });

    // Bar Chart
    new Chart(document.getElementById("barChart"), {
        type: "bar",
        data: {
            labels: ["Low", "Moderate", "High"],
            datasets: [{
                label: "Count",
                data: [dist.low, dist.moderate, dist.high],
                backgroundColor: "#0ea5a4"
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

});
