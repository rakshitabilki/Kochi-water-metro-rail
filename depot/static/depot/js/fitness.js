// Fetch data from Django API (updated to new format)
fetch("/depot/api/fitness/")
    .then(response => response.json())
    .then(data => {
        const items = data.fitness;   // <-- UPDATED
        const boatGrid = document.getElementById('boatGrid');
        const today = new Date();

        items.forEach(item => {
            const validTillDate = new Date(item.valid_to);
            const status = item.isValid ? "Valid" : "Expired";
            const statusClass = (status === "Valid") ? "status-valid" : "status-expired";

            // ✔ SAME SVG ANIMATION — untouched
            const iconSVG = item.isValid
                ? `<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="32" cy="32" r="30" stroke="#45a895" stroke-width="3" fill="none"/>
                        <path d="M20 34l8 8 16-20" stroke="#45a895" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                        <animate attributeName="stroke" values="#45a895;#2176c7;#45a895" dur="3s" repeatCount="indefinite"/>
                   </svg>`
                : `<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="32" cy="32" r="30" stroke="#d62828" stroke-width="3" fill="none"/>
                        <line x1="20" y1="20" x2="44" y2="44" stroke="#d62828" stroke-width="4"/>
                        <line x1="44" y1="20" x2="20" y2="44" stroke="#d62828" stroke-width="4"/>
                   </svg>`;

            const card = document.createElement('div');
            card.classList.add('card');

            // ✔ Updated fields but SAME DESIGN
            card.innerHTML = `
                <div class="icon-container">${iconSVG}</div>
                <h2>${item.train_number} - ${item.train_name || ""}</h2>

                <p><strong>Department</strong>: ${item.department}</p>
                <p><strong>Valid From</strong>: ${item.valid_from}</p>
                <p><strong>Valid Till</strong>: ${item.valid_to}</p>
                <p><strong>Document</strong>: ${item.doc || "None"}</p>

                <p class="${statusClass}">${status}</p>
            `;

            card.style.cursor = "pointer";

            // ✔ Updated click redirect
            card.addEventListener("click", () => {
                window.location.href = `/depot/fitness/${item.train_number}/`;
            });

            boatGrid.appendChild(card);
        });
    })
    .catch(err => console.error("Error loading fitness data:", err));
