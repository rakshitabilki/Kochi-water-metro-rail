console.log("Cleaning JS Loaded");

// DOM references
const boatDetails = document.getElementById("boatDetails");
const slotsTableWrapper = document.getElementById("slotsTableWrapper");

async function loadCleaningData() {
    try {
        const res = await fetch("/depot/api/cleaning/");
        const data = await res.json();
        console.log("API DATA:", data);

        const list = data.cleaning;

        if (!list.length) {
            boatDetails.innerHTML = "<p>No cleaning records available.</p>";
            return;
        }

        // ---------------------------
        // 1️⃣ Build Swipe Cards
        // ---------------------------
        boatDetails.innerHTML = "";
        list.forEach((item, index) => {
            const card = document.createElement("div");
            card.className = "cleaning-card";

            card.innerHTML = `
                <h3>${item.train_number} - ${item.train_name || ""}</h3>
                <p><strong>Bay:</strong> ${item.bay_name} (Position: ${item.bay_position})</p>
                <p><strong>Start Time:</strong> ${item.start_time}</p>
                <p><strong>End Time:</strong> ${item.end_time}</p>
            `;

            boatDetails.appendChild(card);
        });

        // ---------------------------
        // 2️⃣ Build Table
        // ---------------------------
        let tableHTML = `
            <table class="slot-table">
                <thead>
                    <tr>
                        <th>Train Number</th>
                        <th>Train Name</th>
                        <th>Bay</th>
                        <th>Start</th>
                        <th>End</th>
                    </tr>
                </thead>
                <tbody>
        `;

        list.forEach(item => {
            tableHTML += `
                <tr>
                    <td>${item.train_number}</td>
                    <td>${item.train_name || "-"}</td>
                    <td>${item.bay_name}</td>
                    <td>${item.start_time}</td>
                    <td>${item.end_time}</td>
                </tr>
            `;
        });

        tableHTML += "</tbody></table>";

        slotsTableWrapper.innerHTML = tableHTML;

        // ---------------------------
        // 3️⃣ Swipe Animation
        // ---------------------------
        let currentIndex = 0;
        const cards = document.querySelectorAll(".cleaning-card");

        function showCard(i) {
            cards.forEach((c, idx) => {
                c.style.display = (idx === i ? "block" : "none");
            });
        }

        document.getElementById("prevBtn").onclick = () => {
            currentIndex = (currentIndex === 0 ? cards.length - 1 : currentIndex - 1);
            showCard(currentIndex);
        };

        document.getElementById("nextBtn").onclick = () => {
            currentIndex = (currentIndex + 1) % cards.length;
            showCard(currentIndex);
        };

        showCard(currentIndex);  // Show first card

    } catch (err) {
        console.error("Cleaning API Error:", err);
    }
}

loadCleaningData();
