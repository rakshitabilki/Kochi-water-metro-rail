// For demonstration, only navigation/interactivity placeholder
document.addEventListener('DOMContentLoaded', () => {

    // ================================
    // OPTIONAL: Example Dynamic Stats Update via Django API
    // ================================
    /*
    fetch('/api/stats/')
      .then(resp => resp.json())
      .then(data => {
          document.querySelector('.stats div:nth-child(1) h2').textContent = data.passengers;
          document.querySelector('.stats div:nth-child(2) h2').textContent = data.boats;
          document.querySelector('.stats div:nth-child(3) h2').textContent = data.routes;
          document.querySelector('.stats div:nth-child(4) h2').textContent = data.kilometres;
      });
    */

    // ================================
    // MODAL POPUP LOGIC FOR STAT BOXES
    // ================================

    const modal = document.getElementById('infoModal');
    const titleEl = document.getElementById('modalTitle');
    const textEl  = document.getElementById('modalText');
    const closeBtn = modal.querySelector('.closeBtn');

    function openModal(title, text) {
        titleEl.textContent = title || '';
        textEl.textContent = text || '';
        modal.classList.add('show');
        modal.setAttribute('aria-hidden', 'false');
        closeBtn.focus();
    }

    function closeModal() {
        modal.classList.remove('show');
        modal.setAttribute('aria-hidden', 'true');
    }

    // Click / keyboard open events
    document.querySelectorAll('.stat-box').forEach(box => {
        if (!box.hasAttribute('tabindex')) box.setAttribute('tabindex', '0');

        box.style.cursor = 'pointer';

        // On click
        box.addEventListener('click', () => {
            openModal(
                box.getAttribute('data-title'),
                box.getAttribute('data-info')
            );
        });

        // On "Enter" or "Space"
        box.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                openModal(
                    box.getAttribute('data-title'),
                    box.getAttribute('data-info')
                );
            }
        });
    });

    // Close modal via X
    closeBtn.addEventListener('click', closeModal);

    // Click outside modal content to close
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });

    // Esc key closes modal
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            closeModal();
        }
    });

});
