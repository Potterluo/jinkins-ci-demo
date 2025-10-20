/**
 * LLM测试报告JavaScript功能
 * 包含图表初始化、表格切换等功能
 */

// 全局变量
let charts = {};

// 初始化函数
document.addEventListener('DOMContentLoaded', function() {
    // 初始化所有组件
    initializeComponents();

    // 初始化图表
    initializeCharts();
});

/**
 * 初始化UI组件
 */
function initializeComponents() {
    // 如果使用了Preline UI，进行初始化
    if (typeof HSStaticMethods !== 'undefined') {
        setTimeout(function() {
            HSStaticMethods.autoInit();
        }, 100);
    }

    // 为所有切换按钮添加事件监听器
    const toggleButtons = document.querySelectorAll('.btn');
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            toggleTable(this);
        });
    });
}

/**
 * 表格切换功能
 * @param {HTMLElement} element - 切换按钮元素
 */
function toggleTable(element) {
    const tableContainer = element.nextElementSibling;
    const icon = element.querySelector('.chevron-icon');

    if (!tableContainer || !icon) {
        console.warn('Toggle table: Missing required elements');
        return;
    }

    if (tableContainer.classList.contains('hidden')) {
        tableContainer.classList.remove('hidden');
        icon.classList.add('rotated');

        // 更新按钮文本
        updateToggleButtonText(element, '收起');

        // 重新渲染可能隐藏的图表
        refreshHiddenCharts(tableContainer);
    } else {
        tableContainer.classList.add('hidden');
        icon.classList.remove('rotated');

        // 更新按钮文本
        updateToggleButtonText(element, '展开');
    }
}

/**
 * 更新切换按钮文本
 * @param {HTMLElement} element - 按钮元素
 * @param {string} action - 动作（'展开' 或 '收起'）
 */
function updateToggleButtonText(element, action) {
    const currentText = element.innerHTML;
    if (action === '收起') {
        element.innerHTML = currentText.replace('展开', '收起');
    } else {
        element.innerHTML = currentText.replace('收起', '展开');
    }
}

/**
 * 刷新隐藏容器中的图表
 * @param {HTMLElement} container - 容器元素
 */
function refreshHiddenCharts(container) {
    const canvases = container.querySelectorAll('canvas');
    canvases.forEach(canvas => {
        const chartId = canvas.id;
        if (charts[chartId]) {
            charts[chartId].resize();
            charts[chartId].update();
        }
    });
}

/**
 * Chart.js全局配置
 */
function configureChartJS() {
    if (typeof Chart !== 'undefined') {
        Chart.defaults.font.family = "'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif'";
        Chart.defaults.color = '#6b7280';
        Chart.defaults.font.size = 11;
        Chart.defaults.responsive = true;
        Chart.defaults.maintainAspectRatio = false;
    }
}

/**
 * 初始化所有图表
 */
function initializeCharts() {
    // 配置Chart.js
    configureChartJS();

    // 这里可以添加动态创建图表的逻辑
    // 目前图表配置是通过Python生成的内联脚本创建的
    // 未来可以改为通过数据属性配置，然后在这里动态创建
}

/**
 * 创建图表的辅助函数
 * @param {string} canvasId - Canvas元素ID
 * @param {string} type - 图表类型 ('line' 或 'bar')
 * @param {Array} labels - X轴标签
 * @param {Array} data - 数据数组
 * @param {Object} options - 额外配置选项
 */
function createChart(canvasId, type, labels, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) {
        console.warn(`Chart canvas not found: ${canvasId}`);
        return null;
    }

    if (typeof Chart === 'undefined') {
        console.warn('Chart.js not loaded');
        return null;
    }

    // 默认配置
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleFont: {
                    size: 12
                },
                bodyFont: {
                    size: 11
                }
            }
        },
        scales: {
            y: {
                beginAtZero: false,
                grid: {
                    color: 'rgba(0, 0, 0, 0.05)'
                },
                ticks: {
                    font: {
                        size: 10
                    }
                }
            },
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    font: {
                        size: 10
                    },
                    maxRotation: 45,
                    minRotation: 45
                }
            }
        }
    };

    // 合并用户选项
    const chartOptions = mergeOptions(defaultOptions, options);

    // 创建图表配置
    const config = {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: options.label || 'Data',
                data: data,
                borderColor: type === 'line' ? '#2dae7d' : '#2dae7d',
                backgroundColor: type === 'line' ? 'rgba(45, 174, 125, 0.1)' : 'rgba(45, 174, 125, 0.7)',
                borderWidth: 1,
                borderRadius: type === 'bar' ? 4 : 0,
                tension: type === 'line' ? 0.2 : 0,
                fill: type === 'line' ? false : true,
                pointRadius: type === 'line' ? 3 : 0,
                pointHoverRadius: type === 'line' ? 5 : 0
            }]
        },
        options: chartOptions
    };

    // 如果是折线图，添加交互配置
    if (type === 'line') {
        config.options.interaction = {
            mode: 'index',
            intersect: false
        };
    }

    // 创建图表
    const chart = new Chart(canvas, config);
    charts[canvasId] = chart;

    return chart;
}

/**
 * 合并对象配置的辅助函数
 * @param {Object} target - 目标对象
 * @param {Object} source - 源对象
 * @returns {Object} 合并后的对象
 */
function mergeOptions(target, source) {
    const result = JSON.parse(JSON.stringify(target));

    for (const key in source) {
        if (source.hasOwnProperty(key)) {
            if (typeof source[key] === 'object' && source[key] !== null && !Array.isArray(source[key])) {
                result[key] = mergeOptions(result[key] || {}, source[key]);
            } else {
                result[key] = source[key];
            }
        }
    }

    return result;
}

/**
 * 导出功能 - 导出图表为图片
 * @param {string} chartId - 图表ID
 * @param {string} filename - 文件名
 */
function exportChart(chartId, filename) {
    const chart = charts[chartId];
    if (!chart) {
        console.warn(`Chart not found: ${chartId}`);
        return;
    }

    const url = chart.toBase64Image();
    const link = document.createElement('a');
    link.download = filename || `${chartId}.png`;
    link.href = url;
    link.click();
}

/**
 * 响应式处理 - 窗口大小改变时重新调整图表
 */
window.addEventListener('resize', function() {
    Object.keys(charts).forEach(chartId => {
        const chart = charts[chartId];
        if (chart) {
            chart.resize();
        }
    });
});

/**
 * 主题切换功能（可选）
 */
function toggleTheme() {
    document.body.classList.toggle('dark-theme');

    // 重新渲染图表以适应新主题
    Object.keys(charts).forEach(chartId => {
        const chart = charts[chartId];
        if (chart) {
            chart.update();
        }
    });
}

/**
 * 打印功能优化
 */
window.addEventListener('beforeprint', function() {
    // 确保所有图表在打印时正确显示
    Object.keys(charts).forEach(chartId => {
        const chart = charts[chartId];
        if (chart) {
            chart.resize();
        }
    });
});

/**
 * 错误处理
 */
window.addEventListener('error', function(e) {
    console.error('JavaScript error in LLM report:', e.error);
});

/**
 * 性能监控
 */
function reportPerformance() {
    if (performance.timing) {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        console.log(`Page load time: ${loadTime}ms`);
    }
}

// 页面加载完成后报告性能
window.addEventListener('load', reportPerformance);

// 导出全局函数供外部调用
window.LLMReport = {
    createChart,
    exportChart,
    toggleTheme,
    toggleTable,
    charts
};