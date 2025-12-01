console.log("Mileage JS Loaded");

document.addEventListener("DOMContentLoaded", loadMileage);

async function loadMileage() {
    const tbody = document.getElementById("mileageTableBody");

    try {
        const res = await fetch("/depot/api/mileage/");
        const data = await res.json();

        console.log("API:", data);

        const list = data.mileage;
        tbody.innerHTML = "";

        list.forEach(item => {
            const tr = document.createElement("tr");

            tr.innerHTML = `
                <td>${item.train_number}</td>
                <td>${item.train_name || "-"}</td>
                <td>${item.last_mileage}</td>
                <td>${item.cumulative_mileage}</td>
            `;

            tbody.appendChild(tr);
        });

    } catch (err) {
        console.error("Mileage API Error:", err);
    }
}
