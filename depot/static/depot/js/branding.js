console.log("Branding JS Loaded");

document.addEventListener("DOMContentLoaded", async () => {
    const tbody = document.getElementById("brandingTableBody");
    console.log("tbody =", tbody);

    if (!tbody) {
        console.error("ERROR: brandingTableBody NOT FOUND!");
        return;
    }

    try {
        const response = await fetch("/depot/api/branding/");
        const data = await response.json();

        console.log("API Response:", data);

        const list = data.branding || [];

        if (list.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5">No Branding Records Found</td></tr>`;
            return;
        }

        list.forEach(item => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${item.train_number}</td>
                <td>${item.train_name || "-"}</td>
                <td>${item.brand}</td>
                <td>${item.required} hrs</td>
                <td>${item.achieved} hrs</td>
            `;

            tbody.appendChild(row);
        });

    } catch (error) {
        console.error("Branding API Error:", error);
    }
});
