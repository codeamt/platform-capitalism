/**
 * Tab switching functionality for agent cards
 * Handles switching between metrics and decision tree views
 */

/**
 * Initialize tab switching for agent cards
 * Sets up click handlers and initial active state
 */
function initAgentTabs() {
    // Remove existing listeners to prevent duplicates
    const existingTabs = document.querySelectorAll('[data-tab]');
    existingTabs.forEach(tab => {
        const clone = tab.cloneNode(true);
        tab.parentNode.replaceChild(clone, tab);
    });
    
    // Add new listeners
    document.querySelectorAll('[data-tab]').forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            const tabName = tab.getAttribute('data-tab');
            const card = tab.closest('.bg-gray-800');
            
            if (!card) return;
            
            // Hide all panels in this card
            card.querySelectorAll('[role="tabpanel"]').forEach(panel => {
                panel.style.display = 'none';
            });
            
            // Remove active class from all tabs in this card
            card.querySelectorAll('[data-tab]').forEach(t => {
                t.classList.remove('border-b-2', 'border-blue-500', 'text-blue-400');
                t.classList.add('text-gray-400');
            });
            
            // Show selected panel
            const panel = card.querySelector('#' + tabName);
            if (panel) panel.style.display = 'block';
            
            // Add active class to clicked tab
            tab.classList.add('border-b-2', 'border-blue-500', 'text-blue-400');
            tab.classList.remove('text-gray-400');
        });
    });
    
    // Set initial active tab for each card
    document.querySelectorAll('.tab-container').forEach(container => {
        const firstTab = container.querySelector('[data-tab]');
        if (firstTab) {
            firstTab.classList.add('border-b-2', 'border-blue-500', 'text-blue-400');
            firstTab.classList.remove('text-gray-400');
        }
    });
}

// Auto-initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAgentTabs);
} else {
    initAgentTabs();
}

// Re-initialize after HTMX content swaps
document.addEventListener('htmx:afterSwap', function(event) {
    setTimeout(initAgentTabs, 150);
});
