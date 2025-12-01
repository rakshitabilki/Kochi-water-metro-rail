fetch("/depot/api/jobcard/")
    .then(res => res.json())
    .then(data => {
        const list = data.jobcards;
        const grid = document.getElementById("jobGrid");
        grid.innerHTML = "";

        list.forEach(item => {
            const card = document.createElement("div");
            card.className = "boat-card";

            let statusClass =
                item.status.toLowerCase() === "completed"
                    ? "completed"
                    : item.status.toLowerCase() === "in progress"
                        ? "in-progress"
                        : "pending";

            // SAME DESIGN WITH COLORS & ANIMATION
            card.innerHTML = `
                <h2>${item.train_number} - ${item.train_name || ""}</h2>

                <p><strong>Job Card ID:</strong> ${item.jobcard_id}</p>
                <p><strong>Assigned Tasks:</strong> ${item.assigned_task}</p>

                <p><strong>Status:</strong>
                    <span class="status ${statusClass}">
                    ${statusClass === "in-progress" ?
                    `
                        <svg class="gear" viewBox="0 0 64 64">
                            <circle cx="32" cy="32" r="28" stroke="#45a895" stroke-width="4" fill="none"/>
                            <line x1="32" y1="16" x2="32" y2="32"
                                  stroke="#2176c7" stroke-width="4" stroke-linecap="round"/>
                        </svg>
                    ` : ""}
                    ${item.status}
                    </span>
                </p>

                <p><strong>Last Service Date:</strong> ${item.last_service_date || "—"}</p>
                <p><strong>Next Maintenance Date:</strong> ${item.next_maintenance_date || "—"}</p>

                <p><strong>Operator:</strong> ${item.operator || "—"}</p>
                <p><strong>Remarks:</strong> ${item.remarks || "—"}</p>
            `;

            card.style.cursor = "pointer";
            card.onclick = () => {
                window.location.href = `/depot/jobcard/${item.train_number}/`;
            };

            grid.appendChild(card);
        });
    })
    .catch(err => console.error("Error loading job card data:", err));
