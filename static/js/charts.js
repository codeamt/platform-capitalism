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
 * Initialize a multi-line wellbeing trends chart
 * Shows burnout, addiction, resilience, and arousal over time
 * @param {string} canvasId - Canvas element ID
 * @param {Array} ticks - X-axis labels (tick numbers)
 * @param {Array} burnout - Burnout values over time
 * @param {Array} addiction - Addiction values over time
 * @param {Array} resilience - Resilience values over time
 * @param {Array} arousal - Arousal values over time
 */
function initWellbeingTrendsChart(canvasId, ticks, burnout, addiction, resilience, arousal) {
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
                        label: '🔥 Burnout',
                        data: burnout,
                        borderColor: 'rgb(239, 68, 68)',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: false,
                        pointRadius: 3,
                        pointHoverRadius: 6
                    },
                    {
                        label: '🎰 Addiction',
                        data: addiction,
                        borderColor: 'rgb(168, 85, 247)',
                        backgroundColor: 'rgba(168, 85, 247, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: false,
                        pointRadius: 3,
                        pointHoverRadius: 6
                    },
                    {
                        label: '💪 Resilience',
                        data: resilience,
                        borderColor: 'rgb(34, 197, 94)',
                        backgroundColor: 'rgba(34, 197, 94, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: false,
                        pointRadius: 3,
                        pointHoverRadius: 6
                    },
                    {
                        label: '⚡ Arousal',
                        data: arousal,
                        borderColor: 'rgb(59, 130, 246)',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: false,
                        pointRadius: 3,
                        pointHoverRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            color: 'rgb(209, 213, 219)',
                            font: { size: 12 },
                            padding: 15,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(17, 24, 39, 0.95)',
                        titleColor: 'rgb(209, 213, 219)',
                        bodyColor: 'rgb(209, 213, 219)',
                        borderColor: 'rgb(75, 85, 99)',
                        borderWidth: 1,
                        padding: 12,
                        displayColors: true,
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.parsed.y.toFixed(3);
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1,
                        title: {
                            display: true,
                            text: 'Metric Value (0-1)',
                            color: 'rgb(156, 163, 175)',
                            font: { size: 11 }
                        },
                        grid: {
                            color: 'rgba(75, 85, 99, 0.3)'
                        },
                        ticks: {
                            color: 'rgb(156, 163, 175)',
                            font: { size: 10 }
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Simulation Tick',
                            color: 'rgb(156, 163, 175)',
                            font: { size: 11 }
                        },
                        grid: {
                            color: 'rgba(75, 85, 99, 0.3)'
                        },
                        ticks: {
                            color: 'rgb(156, 163, 175)',
                            font: { size: 10 }
                        }
                    }
                }
            }
        });
    }, 100);
}

/**
 * Initialize a system health gauge (semi-circle doughnut chart)
 * @param {string} canvasId - Canvas element ID
 * @param {number} healthScore - Current health score (0-1)
 * @param {number} previousScore - Previous health score for trend indicator
 */
function initSystemHealthGauge(canvasId, healthScore, previousScore) {
    setTimeout(function() {
        const ctx = document.getElementById(canvasId);
        if (!ctx || !window.Chart) return;
        
        // Destroy existing chart if it exists
        const existingChart = Chart.getChart(canvasId);
        if (existingChart) {
            existingChart.destroy();
        }
        
        // Convert to percentage
        const percentage = Math.round(healthScore * 100);
        const remaining = 100 - percentage;
        
        // Determine color based on health score
        let gaugeColor, statusText, statusColor;
        if (healthScore >= 0.7) {
            gaugeColor = 'rgb(34, 197, 94)';
            statusText = 'Healthy';
            statusColor = 'text-green-400';
        } else if (healthScore >= 0.4) {
            gaugeColor = 'rgb(234, 179, 8)';
            statusText = 'Warning';
            statusColor = 'text-yellow-400';
        } else {
            gaugeColor = 'rgb(239, 68, 68)';
            statusText = 'Critical';
            statusColor = 'text-red-400';
        }
        
        // Calculate trend
        const trend = previousScore !== null ? healthScore - previousScore : 0;
        const trendIcon = trend > 0.01 ? '↑' : trend < -0.01 ? '↓' : '→';
        const trendColor = trend > 0.01 ? 'rgb(34, 197, 94)' : trend < -0.01 ? 'rgb(239, 68, 68)' : 'rgb(156, 163, 175)';
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [percentage, remaining],
                    backgroundColor: [gaugeColor, 'rgba(55, 65, 81, 0.3)'],
                    borderColor: ['rgba(0, 0, 0, 0.1)', 'rgba(0, 0, 0, 0.1)'],
                    borderWidth: 2,
                    circumference: 180,
                    rotation: 270
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: false
                    }
                },
                cutout: '75%'
            },
            plugins: [{
                id: 'gaugeText',
                afterDraw: function(chart) {
                    const ctx = chart.ctx;
                    const centerX = chart.chartArea.left + (chart.chartArea.right - chart.chartArea.left) / 2;
                    const centerY = chart.chartArea.top + (chart.chartArea.bottom - chart.chartArea.top) / 2 + 20;
                    
                    // Draw percentage
                    ctx.save();
                    ctx.font = 'bold 48px sans-serif';
                    ctx.fillStyle = gaugeColor;
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(percentage, centerX, centerY - 10);
                    
                    // Draw status text
                    ctx.font = '14px sans-serif';
                    ctx.fillStyle = 'rgb(156, 163, 175)';
                    ctx.fillText(statusText, centerX, centerY + 30);
                    
                    // Draw trend indicator
                    if (previousScore !== null) {
                        ctx.font = 'bold 20px sans-serif';
                        ctx.fillStyle = trendColor;
                        ctx.fillText(trendIcon, centerX + 40, centerY - 10);
                    }
                    
                    ctx.restore();
                }
            }]
        });
    }, 100);
}

/**
 * Initialize agent trait distribution chart with bars and individual points
 * @param {string} canvasId - Canvas element ID
 * @param {Object} traitData - Object with trait names as keys and arrays of values
 * Example: { Burnout: [0.2, 0.3, ...], Addiction: [...], Resilience: [...], Arousal: [...] }
 */
function initAgentTraitBoxPlots(canvasId, traitData) {
    setTimeout(function() {
        const ctx = document.getElementById(canvasId);
        if (!ctx || !window.Chart) return;
        
        // Destroy existing chart if it exists
        const existingChart = Chart.getChart(canvasId);
        if (existingChart) {
            existingChart.destroy();
        }
        
        // Calculate statistics
        function calculateStats(values) {
            const n = values.length;
            const mean = values.reduce((a, b) => a + b, 0) / n;
            const variance = values.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / n;
            const std = Math.sqrt(variance);
            const sorted = [...values].sort((a, b) => a - b);
            
            return {
                mean: mean,
                std: std,
                min: sorted[0],
                max: sorted[n - 1],
                median: sorted[Math.floor(n * 0.5)]
            };
        }
        
        const labels = Object.keys(traitData);
        const stats = {};
        labels.forEach(label => {
            stats[label] = calculateStats(traitData[label]);
        });
        
        // Color mapping
        const colorMap = {
            'Burnout': { bar: 'rgba(239, 68, 68, 0.6)', border: 'rgb(239, 68, 68)', points: 'rgba(248, 113, 113, 0.8)' },
            'Addiction': { bar: 'rgba(168, 85, 247, 0.6)', border: 'rgb(168, 85, 247)', points: 'rgba(192, 132, 252, 0.8)' },
            'Resilience': { bar: 'rgba(34, 197, 94, 0.6)', border: 'rgb(34, 197, 94)', points: 'rgba(74, 222, 128, 0.8)' },
            'Arousal': { bar: 'rgba(59, 130, 246, 0.6)', border: 'rgb(59, 130, 246)', points: 'rgba(96, 165, 250, 0.8)' }
        };
        
        // Create datasets
        const barDataset = {
            label: 'Mean Value',
            data: labels.map(label => stats[label].mean),
            backgroundColor: labels.map(label => colorMap[label].bar),
            borderColor: labels.map(label => colorMap[label].border),
            borderWidth: 2,
            type: 'bar',
            order: 2
        };
        
        // Individual agent points as scatter overlay
        const scatterDatasets = labels.map((label, idx) => ({
            label: label + ' (agents)',
            data: traitData[label].map(value => ({ x: idx, y: value })),
            backgroundColor: colorMap[label].points,
            borderColor: colorMap[label].border,
            borderWidth: 1,
            pointRadius: 4,
            pointHoverRadius: 6,
            type: 'scatter',
            order: 1,
            showLine: false
        }));
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [barDataset, ...scatterDatasets]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'point',
                    intersect: true
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            color: 'rgb(209, 213, 219)',
                            font: { size: 11 },
                            filter: function(item) {
                                // Only show mean value in legend
                                return item.text === 'Mean Value';
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(17, 24, 39, 0.95)',
                        titleColor: 'rgb(209, 213, 219)',
                        bodyColor: 'rgb(209, 213, 219)',
                        borderColor: 'rgb(75, 85, 99)',
                        borderWidth: 1,
                        padding: 12,
                        callbacks: {
                            title: function(context) {
                                return context[0].label;
                            },
                            label: function(context) {
                                const label = context.dataset.label;
                                if (label === 'Mean Value') {
                                    const traitLabel = context.label;
                                    const s = stats[traitLabel];
                                    return [
                                        'Mean: ' + s.mean.toFixed(3),
                                        'Std Dev: ±' + s.std.toFixed(3),
                                        'Range: [' + s.min.toFixed(3) + ' - ' + s.max.toFixed(3) + ']',
                                        'Median: ' + s.median.toFixed(3)
                                    ];
                                } else {
                                    return 'Agent value: ' + context.parsed.y.toFixed(3);
                                }
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Creator Traits',
                            color: 'rgb(156, 163, 175)',
                            font: { size: 12, weight: 'bold' }
                        },
                        grid: {
                            color: 'rgba(75, 85, 99, 0.2)'
                        },
                        ticks: {
                            color: 'rgb(209, 213, 219)',
                            font: { size: 11 }
                        }
                    },
                    y: {
                        beginAtZero: true,
                        max: 1,
                        title: {
                            display: true,
                            text: 'Trait Value (0-1)',
                            color: 'rgb(156, 163, 175)',
                            font: { size: 12, weight: 'bold' }
                        },
                        grid: {
                            color: 'rgba(75, 85, 99, 0.3)'
                        },
                        ticks: {
                            color: 'rgb(156, 163, 175)',
                            font: { size: 10 },
                            stepSize: 0.2
                        }
                    }
                }
            },
            plugins: [{
                id: 'errorBars',
                afterDatasetsDraw: function(chart) {
                    const ctx = chart.ctx;
                    const xScale = chart.scales.x;
                    const yScale = chart.scales.y;
                    
                    labels.forEach((label, idx) => {
                        const s = stats[label];
                        const x = xScale.getPixelForValue(idx);
                        const mean = yScale.getPixelForValue(s.mean);
                        const top = yScale.getPixelForValue(Math.min(s.mean + s.std, 1));
                        const bottom = yScale.getPixelForValue(Math.max(s.mean - s.std, 0));
                        
                        ctx.save();
                        ctx.strokeStyle = colorMap[label].border;
                        ctx.lineWidth = 2;
                        
                        // Draw error bar (±1 std)
                        ctx.beginPath();
                        ctx.moveTo(x, bottom);
                        ctx.lineTo(x, top);
                        ctx.stroke();
                        
                        // Draw caps
                        ctx.beginPath();
                        ctx.moveTo(x - 8, top);
                        ctx.lineTo(x + 8, top);
                        ctx.moveTo(x - 8, bottom);
                        ctx.lineTo(x + 8, bottom);
                        ctx.stroke();
                        
                        ctx.restore();
                    });
                }
            }]
        });
    }, 100);
}

/**
 * Initialize reward characteristics panel (histogram + stats)
 * @param {string} canvasId - Canvas element ID
 * @param {Array} rewards - Array of all reward values
 * @param {number} avgReward - Average reward
 * @param {number} variance - Reward variance
 * @param {number} predictability - Reward predictability score
 */
function initRewardCharacteristics(canvasId, rewards, avgReward, variance, predictability) {
    setTimeout(function() {
        const ctx = document.getElementById(canvasId);
        if (!ctx || !window.Chart) return;
        
        // Destroy existing chart if it exists
        const existingChart = Chart.getChart(canvasId);
        if (existingChart) {
            existingChart.destroy();
        }
        
        // Create histogram bins
        const bins = 10;
        const min = Math.min(...rewards);
        const max = Math.max(...rewards);
        const binSize = (max - min) / bins;
        const histogram = new Array(bins).fill(0);
        const binLabels = [];
        
        for (let i = 0; i < bins; i++) {
            const binStart = min + i * binSize;
            const binEnd = binStart + binSize;
            binLabels.push(binStart.toFixed(2));
            
            rewards.forEach(r => {
                if (r >= binStart && (i === bins - 1 ? r <= binEnd : r < binEnd)) {
                    histogram[i]++;
                }
            });
        }
        
        // Determine color based on average reward
        const barColor = avgReward > 0 ? 'rgba(34, 197, 94, 0.7)' : 'rgba(239, 68, 68, 0.7)';
        const borderColor = avgReward > 0 ? 'rgb(34, 197, 94)' : 'rgb(239, 68, 68)';
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: binLabels,
                datasets: [{
                    label: 'Reward Frequency',
                    data: histogram,
                    backgroundColor: barColor,
                    borderColor: borderColor,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(17, 24, 39, 0.95)',
                        titleColor: 'rgb(209, 213, 219)',
                        bodyColor: 'rgb(209, 213, 219)',
                        borderColor: 'rgb(75, 85, 99)',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                return 'Count: ' + context.parsed.y + ' agents';
                            }
                        }
                    },
                    title: {
                        display: true,
                        text: [
                            'Avg: ' + avgReward.toFixed(3) + ' | Variance: ' + variance.toFixed(3),
                            'Predictability: ' + (predictability * 100).toFixed(1) + '%'
                        ],
                        color: 'rgb(209, 213, 219)',
                        font: { size: 11 },
                        padding: { top: 5, bottom: 10 }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Reward Value',
                            color: 'rgb(156, 163, 175)',
                            font: { size: 11 }
                        },
                        grid: {
                            color: 'rgba(75, 85, 99, 0.2)'
                        },
                        ticks: {
                            color: 'rgb(156, 163, 175)',
                            font: { size: 9 },
                            maxRotation: 45,
                            minRotation: 45
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Frequency',
                            color: 'rgb(156, 163, 175)',
                            font: { size: 11 }
                        },
                        grid: {
                            color: 'rgba(75, 85, 99, 0.3)'
                        },
                        ticks: {
                            color: 'rgb(156, 163, 175)',
                            font: { size: 9 },
                            precision: 0
                        }
                    }
                }
            }
        });
    }, 100);
}

/**
 * Initialize state transition flow (Sankey-style bar chart)
 * @param {string} canvasId - Canvas element ID
 * @param {Object} transitions - Object with state transition counts
 * Example: { "OPTIMIZER->HUSTLER": 5, "HUSTLER->BURNED_OUT": 3, ... }
 */
function initStateTransitionFlow(canvasId, transitions) {
    setTimeout(function() {
        const ctx = document.getElementById(canvasId);
        if (!ctx || !window.Chart) return;
        
        // Destroy existing chart if it exists
        const existingChart = Chart.getChart(canvasId);
        if (existingChart) {
            existingChart.destroy();
        }
        
        // Sort transitions by count
        const sortedTransitions = Object.entries(transitions)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 8); // Top 8 transitions
        
        const labels = sortedTransitions.map(([key]) => key.replace('->', ' → '));
        const data = sortedTransitions.map(([, value]) => value);
        
        // Color by transition type
        const colors = labels.map(label => {
            if (label.includes('BURNED_OUT') || label.includes('ADDICTED')) {
                return 'rgba(239, 68, 68, 0.7)';
            } else if (label.includes('RESILIENT') || label.includes('OPTIMIZER')) {
                return 'rgba(34, 197, 94, 0.7)';
            } else {
                return 'rgba(234, 179, 8, 0.7)';
            }
        });
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Transitions',
                    data: data,
                    backgroundColor: colors,
                    borderColor: colors.map(c => c.replace('0.7', '1')),
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(17, 24, 39, 0.95)',
                        titleColor: 'rgb(209, 213, 219)',
                        bodyColor: 'rgb(209, 213, 219)',
                        borderColor: 'rgb(75, 85, 99)',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                return 'Count: ' + context.parsed.x + ' transitions';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Transition Count',
                            color: 'rgb(156, 163, 175)',
                            font: { size: 11 }
                        },
                        grid: {
                            color: 'rgba(75, 85, 99, 0.3)'
                        },
                        ticks: {
                            color: 'rgb(156, 163, 175)',
                            font: { size: 9 },
                            precision: 0
                        }
                    },
                    y: {
                        grid: {
                            color: 'rgba(75, 85, 99, 0.2)'
                        },
                        ticks: {
                            color: 'rgb(209, 213, 219)',
                            font: { size: 10 }
                        }
                    }
                }
            }
        });
    }, 100);
}

/**
 * Initialize correlation heatmap
 * @param {string} canvasId - Canvas element ID
 * @param {Object} correlations - Correlation matrix data
 * Example: { burnout_addiction: 0.75, burnout_resilience: -0.6, ... }
 */
function initCorrelationHeatmap(canvasId, correlations) {
    setTimeout(function() {
        const ctx = document.getElementById(canvasId);
        if (!ctx || !window.Chart) return;
        
        // Destroy existing chart if it exists
        const existingChart = Chart.getChart(canvasId);
        if (existingChart) {
            existingChart.destroy();
        }
        
        // Define metrics
        const metrics = ['Burnout', 'Addiction', 'Resilience', 'Arousal'];
        const data = [];
        
        // Build correlation matrix
        for (let i = 0; i < metrics.length; i++) {
            for (let j = 0; j < metrics.length; j++) {
                if (i !== j) {
                    const key1 = metrics[i] + '_' + metrics[j];
                    const key2 = metrics[j] + '_' + metrics[i];
                    const corr = correlations[key1] || correlations[key2] || 0;
                    
                    data.push({
                        x: metrics[j],
                        y: metrics[i],
                        v: corr
                    });
                }
            }
        }
        
        // Color scale function
        function getColor(value) {
            if (value > 0.5) return 'rgba(239, 68, 68, ' + (0.5 + value * 0.5) + ')';
            if (value > 0) return 'rgba(234, 179, 8, ' + (0.3 + value * 0.5) + ')';
            if (value > -0.5) return 'rgba(59, 130, 246, ' + (0.3 + Math.abs(value) * 0.5) + ')';
            return 'rgba(34, 197, 94, ' + (0.5 + Math.abs(value) * 0.5) + ')';
        }
        
        new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: data.map(point => ({
                    label: point.y + ' vs ' + point.x,
                    data: [{ x: point.x, y: point.y }],
                    backgroundColor: getColor(point.v),
                    borderColor: 'rgba(0, 0, 0, 0.2)',
                    borderWidth: 1,
                    pointRadius: 25,
                    pointHoverRadius: 28,
                    correlation: point.v
                }))
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(17, 24, 39, 0.95)',
                        titleColor: 'rgb(209, 213, 219)',
                        bodyColor: 'rgb(209, 213, 219)',
                        borderColor: 'rgb(75, 85, 99)',
                        borderWidth: 1,
                        callbacks: {
                            title: function(context) {
                                return context[0].dataset.label;
                            },
                            label: function(context) {
                                const corr = context.dataset.correlation;
                                const strength = Math.abs(corr) > 0.7 ? 'Strong' : 
                                               Math.abs(corr) > 0.4 ? 'Moderate' : 'Weak';
                                const direction = corr > 0 ? 'positive' : 'negative';
                                return [
                                    'Correlation: ' + corr.toFixed(3),
                                    strength + ' ' + direction + ' relationship'
                                ];
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        type: 'category',
                        labels: metrics,
                        grid: {
                            color: 'rgba(75, 85, 99, 0.3)'
                        },
                        ticks: {
                            color: 'rgb(209, 213, 219)',
                            font: { size: 10 }
                        }
                    },
                    y: {
                        type: 'category',
                        labels: metrics,
                        grid: {
                            color: 'rgba(75, 85, 99, 0.3)'
                        },
                        ticks: {
                            color: 'rgb(209, 213, 219)',
                            font: { size: 10 }
                        }
                    }
                }
            },
            plugins: [{
                id: 'correlationText',
                afterDatasetsDraw: function(chart) {
                    const ctx = chart.ctx;
                    chart.data.datasets.forEach((dataset, i) => {
                        const meta = chart.getDatasetMeta(i);
                        if (!meta.hidden && meta.data[0]) {
                            const element = meta.data[0];
                            const corr = dataset.correlation;
                            
                            ctx.save();
                            ctx.font = 'bold 11px sans-serif';
                            ctx.fillStyle = Math.abs(corr) > 0.5 ? 'white' : 'rgb(209, 213, 219)';
                            ctx.textAlign = 'center';
                            ctx.textBaseline = 'middle';
                            ctx.fillText(corr.toFixed(2), element.x, element.y);
                            ctx.restore();
                        }
                    });
                }
            }]
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
