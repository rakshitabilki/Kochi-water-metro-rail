console.log("Geometry JS Loaded");

// Fetch data + render both swiper and table
async function loadGeometryData() {
    try {
        const response = await fetch("/depot/api/geometry/");
        const data = await response.json();

        console.log("Geometry API Response:", data);

        const list = data.geometry;

        // --- DOM elements ---
        const swiper = document.getElementById("boatDetails");
        const tableWrapper = document.getElementById("slotsTableWrapper");

        if (!swiper) {
            console.error("ERROR: #boatDetails not found");
            return;
        }
        if (!tableWrapper) {
            console.error("ERROR: #slotsTableWrapper not found");
            return;
        }

        // Clear
        swiper.innerHTML = "";
        tableWrapper.innerHTML = "";

        // ---------------------------
        // 🔵 1. Build Swiper Cards
        // ---------------------------
        list.forEach(item => {
            const card = document.createElement("div");

            // FIXED → Correct CSS classes
            card.className = "swiper-card";

            card.innerHTML = `
                <h2>${item.train_number} - ${item.train_name || "-"}</h2>
                <p><strong>Stabling Bay:</strong> ${item.bay_name || "-"}</p>
                <p><strong>Bay Position:</strong> ${item.bay_position ?? "-"}</p>
                <p><strong>Bay Capacity:</strong> ${item.bay_capacity ?? "-"}</p>
            `;

            swiper.appendChild(card);
        });

        // ---------------------------
        // 🔵 2. Build Table View
        // ---------------------------
        let html = `
            <table class="slots-table">   <!-- FIXED: Added class -->
                <thead>
                    <tr>
                        <th>Train Number</th>
                        <th>Train Name</th>
                        <th>Bay Name</th>
                        <th>Position</th>
                        <th>Capacity</th>
                    </tr>
                </thead>
                <tbody>
        `;

        list.forEach(item => {
            html += `
                <tr>
                    <td>${item.train_number}</td>
                    <td>${item.train_name || "-"}</td>
                    <td>${item.bay_name || "-"}</td>
                    <td>${item.bay_position ?? "-"}</td>
                    <td>${item.bay_capacity ?? "-"}</td>
                </tr>
            `;
        });

        html += `</tbody></table>`;
        tableWrapper.innerHTML = html;

        // ---------------------------
        // 🔵 3. Add Swiper Functionality
        // ---------------------------

        let index = 0;
        const cards = document.querySelectorAll(".swiper-card");

        function showCard(i) {
            cards.forEach((c, idx) => {
                c.style.display = idx === i ? "block" : "none";
            });
        }

        showCard(index);

        document.getElementById("prevBtn").onclick = () => {
            index = (index - 1 + cards.length) % cards.length;
            showCard(index);
        };

        document.getElementById("nextBtn").onclick = () => {
            index = (index + 1) % cards.length;
            showCard(index);
        };

    } catch (err) {
        console.error("Geometry API Error:", err);
    }
}

loadGeometryData();
