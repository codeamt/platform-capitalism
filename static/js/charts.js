/**
 * Chart initialization utilities for Platform Capitalism simulation
 * Handles Chart.js initialization with proper cleanup and error handling
 */

/**
 * Initialize a pie chart for agent distribution
 * @param {string} canvasId - Canvas element ID
 * @param {Array} labels - Chart labels
 * @param {Array} data - Chart data values
 * @param {Array} colors - Background colors for each segment
 */
function initAgentDistributionPie(canvasId, labels, data, colors) {
    setTimeout(function() {
        const ctx = document.getElementById(canvasId);
        if (!ctx || !window.Chart) return;
        
        // Destroy existing chart if it exists
        const existingChart = Chart.getChart(canvasId);
        if (existingChart) {
            existingChart.destroy();
        }
        
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors,
                    borderColor: 'rgb(31, 41, 55)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'right',
                        labels: {
                            color: 'rgb(209, 213, 219)',
                            font: { size: 12 }
                        }
                    }
                }
            }
        });
    }, 100);
}

/**
 * Initialize a line chart for arousal trend
 * @param {string} canvasId - Canvas element ID
 * @param {Array} ticks - X-axis labels (tick numbers)
 * @param {Array} arousal - Y-axis data (arousal values)
 */
function initArousalTrendChart(canvasId, ticks, arousal) {
    setTimeout(function() {
        const ctx = document.getElementById(canvasId);
        if (!ctx || !window.Chart) return;
        
        // Destroy existing chart if it exists
        const existingChart = Chart.getChart(canvasId);
        if (existingChart) {
            existingChart.destroy();
        }
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ticks,
                datasets: [
                    {
                        label: 'Arousal',
                        data: arousal,
                        borderColor: 'rgb(59, 130, 246)',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.3,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            color: 'rgb(209, 213, 219)',
                            font: { size: 12 }
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1,
                        grid: {
                            color: 'rgba(75, 85, 99, 0.3)'
                        },
                        ticks: {
                            color: 'rgb(156, 163, 175)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(75, 85, 99, 0.3)'
                        },
                        ticks: {
                            color: 'rgb(156, 163, 175)'
                        }
                    }
                }
            }
        });
    }, 100);
}

/**
 * Initialize a reward timeline chart with mean line
 * @param {string} canvasId - Canvas element ID
 * @param {Array} ticks - X-axis labels
 * @param {Array} rewards - Actual reward values
 * @param {Array} meanLine - Mean reward line values
 * @param {string} lineColor - Color for the reward line
 */
function initRewardTimelineChart(canvasId, ticks, rewards, meanLine, lineColor) {
    setTimeout(function() {
        const ctx = document.getElementById(canvasId);
        if (!ctx || !window.Chart) return;
        
        // Destroy existing chart if it exists
        const existingChart = Chart.getChart(canvasId);
        if (existingChart) {
            existingChart.destroy();
        }
        
        // Convert rgb to rgba for fill
        const fillColor = lineColor.replace('rgb', 'rgba').replace(')', ', 0.1)');
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ticks,
                datasets: [
                    {
                        label: 'Actual Rewards',
                        data: rewards,
                        borderColor: lineColor,
                        backgroundColor: fillColor,
                        borderWidth: 2,
                        tension: 0.3,
                        fill: true,
                        pointRadius: 3,
                        pointHoverRadius: 5
                    },
                    {
                        label: 'Mean Reward',
                        data: meanLine,
                        borderColor: 'rgb(156, 163, 175)',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        fill: false,
                        pointRadius: 0
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Average Reward'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Tick'
                        }
                    }
                }
            }
        });
    }, 100);
}
