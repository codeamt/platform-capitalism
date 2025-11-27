/**
 * Agent sparkline chart utilities
 * Creates small inline charts for agent burnout and reward history
 */

/**
 * Initialize burnout sparkline for an agent
 * @param {string} agentId - Agent identifier
 * @param {Array} ticks - Tick numbers
 * @param {Array} burnoutHistory - Burnout values over time
 */
function initBurnoutSparkline(agentId, ticks, burnoutHistory) {
    setTimeout(function() {
        const ctx = document.getElementById('burnout-' + agentId);
        if (!ctx || !window.Chart) return;
        
        // Destroy existing chart if it exists
        const existingChart = Chart.getChart('burnout-' + agentId);
        if (existingChart) {
            existingChart.destroy();
        }
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ticks,
                datasets: [{
                    data: burnoutHistory,
                    borderColor: 'rgb(239, 68, 68)',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderWidth: 1.5,
                    pointRadius: 0,
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { display: false },
                    y: { display: false, min: 0, max: 1 }
                }
            }
        });
    }, 100);
}

/**
 * Initialize reward sparkline for an agent
 * @param {string} agentId - Agent identifier
 * @param {Array} ticks - Tick numbers
 * @param {Array} rewardHistory - Reward values over time
 */
function initRewardSparkline(agentId, ticks, rewardHistory) {
    setTimeout(function() {
        const ctx = document.getElementById('reward-' + agentId);
        if (!ctx || !window.Chart) return;
        
        // Destroy existing chart if it exists
        const existingChart = Chart.getChart('reward-' + agentId);
        if (existingChart) {
            existingChart.destroy();
        }
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ticks,
                datasets: [{
                    data: rewardHistory,
                    borderColor: 'rgb(34, 197, 94)',
                    backgroundColor: 'rgba(34, 197, 94, 0.1)',
                    borderWidth: 1.5,
                    pointRadius: 0,
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { display: false },
                    y: { display: false, min: 0 }
                }
            }
        });
    }, 100);
}
