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
                    borderColor: 'rgb(248, 113, 113)',
                    backgroundColor: 'rgba(239, 68, 68, 0.2)',
                    borderWidth: 2,
                    pointRadius: 2,
                    pointHoverRadius: 5,
                    pointBackgroundColor: 'rgb(239, 68, 68)',
                    pointBorderColor: 'rgb(248, 113, 113)',
                    pointBorderWidth: 2,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { 
                    legend: { display: false },
                    tooltip: {
                        enabled: true,
                        backgroundColor: 'rgba(17, 24, 39, 0.9)',
                        titleColor: 'rgb(248, 113, 113)',
                        bodyColor: 'rgb(209, 213, 219)',
                        borderColor: 'rgb(239, 68, 68)',
                        borderWidth: 1,
                        displayColors: false,
                        callbacks: {
                            label: function(context) {
                                return 'Burnout: ' + context.parsed.y.toFixed(2);
                            }
                        }
                    }
                },
                scales: {
                    x: { display: false },
                    y: { display: false, min: 0, max: 1 }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
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
                    borderColor: 'rgb(52, 211, 153)',
                    backgroundColor: 'rgba(34, 197, 94, 0.2)',
                    borderWidth: 2,
                    pointRadius: 2,
                    pointHoverRadius: 5,
                    pointBackgroundColor: 'rgb(34, 197, 94)',
                    pointBorderColor: 'rgb(52, 211, 153)',
                    pointBorderWidth: 2,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { 
                    legend: { display: false },
                    tooltip: {
                        enabled: true,
                        backgroundColor: 'rgba(17, 24, 39, 0.9)',
                        titleColor: 'rgb(52, 211, 153)',
                        bodyColor: 'rgb(209, 213, 219)',
                        borderColor: 'rgb(34, 197, 94)',
                        borderWidth: 1,
                        displayColors: false,
                        callbacks: {
                            label: function(context) {
                                return 'Reward: ' + context.parsed.y.toFixed(2);
                            }
                        }
                    }
                },
                scales: {
                    x: { display: false },
                    y: { display: false, min: 0 }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                }
            }
        });
    }, 100);
}
