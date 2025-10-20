"""
Standalone LLM Test Report Generator
Generates an HTML report with LLM benchmark data for local testing
"""

import json
import os
from pathlib import Path
from datetime import datetime


class LLMReportGenerator:
    def __init__(self, data_dir=None):
        if data_dir is None:
            # 默认数据目录路径
            self.data_dir = Path(__file__).parent.parent / "data"
        else:
            # 处理相对路径
            if isinstance(data_dir, str):
                data_dir = Path(data_dir)
            # 如果是相对路径，基于当前工作目录
            if not data_dir.is_absolute():
                data_dir = Path.cwd() / data_dir
            self.data_dir = data_dir
        self.test_data = {}
        self.load_all_data()
        print(f"Data directory set to: {self.data_dir}")
        print(f"Data directory exists: {self.data_dir.exists()}")
    
    def load_all_data(self):
        """Load all JSON files from the data directory"""
        if not self.data_dir.exists():
            print(f"Warning: Data directory {self.data_dir} not found")
            return
        
        for json_file in self.data_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    tool_name = data.get('tool', json_file.stem)
                    self.test_data[tool_name] = data
                    print(f"Loaded data for {tool_name}")
            except Exception as e:
                print(f"Warning: Could not load {json_file}: {e}")
    
    def generate_html_report(self, output_file="llm_test_report_demo.html"):
        """Generate a complete HTML report with modern design"""
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLM测试报告</title>
    
    <!-- Preline UI CDN -->
    <script src="https://cdn.jsdelivr.net/npm/preline@2.3.0/dist/preline.js"></script>

    <!-- Font Awesome CDN -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <!-- 外部CSS文件 -->
    <link rel="stylesheet" href="./llm_report_styles.css">

    <!-- 添加animate.css CDN以支持动画效果 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
</head>
<body>
    <!-- Header -->
    <header>
        <div class="container">
            <div class="footer-content">
                <div>
                    <h1>🤖 LLM测试报告</h1>
                    <p class="text-gray-600 mt-1">AI模型性能与准确性基准测试</p>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="container py-8">
        <!-- Tool List -->
        <div style="display: flex; flex-direction: column; gap: 1.5rem;">
            {self.generate_tool_cards()}
        </div>
    </main>

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="footer-content">
                <p class="footer-text">
                    生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </p>
                <p class="footer-text mt-2">
                    © 2025 LLM测试框架
                </p>
            </div>
        </div>
    </footer>

    <!-- 外部JavaScript文件 -->
    <script src="./llm_report_scripts.js"></script>

    <!-- 图表初始化脚本 -->
    <script>
        // Chart.js global configuration
        if (typeof Chart !== 'undefined') {{
            Chart.defaults.font.family = "'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif'";
            Chart.defaults.color = '#6b7280';
            Chart.defaults.font.size = 11;
        }}

        {self.generate_chart_scripts()}
    </script>
</body>
</html>"""
        
        # 确保输出目录存在
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # 复制CSS和JS文件到reports目录
        self.copy_static_files(output_path.parent)

        print(f"HTML report generated: {output_file}")
        return output_file

    def copy_static_files(self, output_dir):
        """Copy static CSS and JS files to the output directory"""
        # 获取当前脚本所在目录
        current_dir = Path(__file__).parent
        static_dir = current_dir.parent / "reports"

        # 要复制的文件列表
        static_files = [
            "llm_report_styles.css",
            "llm_report_scripts.js"
        ]

        for filename in static_files:
            source_file = static_dir / filename
            target_file = output_dir / filename

            if source_file.exists():
                try:
                    # 先读取源文件内容，然后写入目标文件
                    with open(source_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    with open(target_file, 'w', encoding='utf-8') as f:
                        f.write(content)

                    print(f"Copied {filename} to {target_file}")
                except Exception as e:
                    print(f"Warning: Failed to copy {filename}: {e}")
            else:
                print(f"Warning: Static file not found: {source_file}")
    
    def generate_tool_cards(self):
        """Generate HTML cards for each tool"""
        if not self.test_data:
            return '<div class="w-full"><div class="bg-white rounded-xl shadow-sm p-8 text-center"><p class="text-gray-500">暂无LLM测试数据，请确保JSON文件位于llm_test_data目录中。</p></div></div>'
        
        cards = []
        for i, (tool_name, tool_data) in enumerate(self.test_data.items()):
            card = self.generate_tool_card(tool_name, tool_data, i)
            cards.append(card)
        
        return '\n'.join(cards)
    
    def generate_tool_card(self, tool_name, tool_data, index):
        """Generate HTML for a single tool card"""
        tool_id = tool_name.lower().replace(" ", "-")
        return f"""
            <div class="card animate-fade-in">
                <div class="card-content">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                        <h2>{tool_data['tool']}</h2>
                        <div class="icon-container">
                            <i class="fas fa-chart-bar"></i>
                        </div>
                    </div>

                    <!-- Metrics Table -->
                    <div class="mb-6">
                        {self.generate_metrics_table(tool_data['runs'], tool_data['metrics_schema'])}
                    </div>

                    <!-- Charts Section Toggle -->
                    <div class="mt-6">
                        <button class="btn">
                            <span class="font-medium">📈 关键指标趋势</span>
                            <i class="fas fa-chevron-down text-gray-500"></i>
                        </button>
                        <div class="hidden mt-3">
                            <div style="display: flex; flex-direction: column; gap: 1rem;">
                                {self.generate_charts(tool_data['runs'], tool_data['metrics_schema'])}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        """
    
    def generate_metrics_table(self, runs, metrics_schema):
        """Generate HTML table for metrics"""
        if not runs:
            return '<div class="text-center py-4 text-gray-500 dark:text-neutral-400">暂无运行数据</div>'
        
        # Table headers - show all metrics for this tool
        headers = ['构建ID', '日期']
        for metric in metrics_schema:
            headers.append(f"{metric['display_name']} ({metric['unit']})")
        
        # Table rows
        rows = []
        for run in sorted(runs, key=lambda x: x['timestamp']):
            row_cells = [
                f'<td style="font-weight: 500;">{run["build_id"]}</td>',
                f'<td style="color: #6b7280;">{run["timestamp"][:10]}</td>'
            ]
            
            # Show all metrics for this run
            for metric in metrics_schema:
                metric_name = metric['name']
                value = run['metrics'].get(metric_name, 'N/A')
                if value != 'N/A':
                    formatted_value = metric['format'].format(value)
                    # No color coding, just display the value
                    row_cells.append(f'<td>{formatted_value}</td>')
                else:
                    row_cells.append('<td style="color: #6b7280;">N/A</td>')
            
            rows.append(f'<tr>{"".join(row_cells)}</tr>')
        
        return f"""
        <div class="table-container">
            <table class="table">
                <thead>
                    <tr>
                        {"".join(f'<th>{header}</th>' for header in headers)}
                    </tr>
                </thead>
                <tbody>
                    {"".join(rows)}
                </tbody>
            </table>
        </div>
        """
    
    def generate_charts(self, runs, metrics_schema):
        """Generate chart containers for key metrics"""
        if not runs:
            return '<div class="text-center py-4 text-gray-500 dark:text-neutral-400">暂无图表数据</div>'
        
        charts_html = []
        
        # Select key metrics for charts
        key_metrics = []
        priority_metrics = ['TTFT', 'Throughput', 'accuracy', 'f1_score']
        
        # Add priority metrics first
        for metric_name in priority_metrics:
            for metric in metrics_schema:
                if metric['name'] == metric_name and len(key_metrics) < 2:
                    key_metrics.append(metric)
        
        # Fill with other metrics if needed
        for metric in metrics_schema:
            if len(key_metrics) >= 2:
                break
            if not any(m['name'] == metric['name'] for m in key_metrics):
                key_metrics.append(metric)
        
        # Generate charts for selected metrics
        for metric in key_metrics:
            chart_type = metric.get('default_chart_type')
            if chart_type in ['line', 'bar']:
                chart_html = self.generate_chart_container(runs, metric, chart_type)
                charts_html.append(chart_html)
        
        return '\n'.join(charts_html) if charts_html else '<div class="text-center py-4 text-gray-500 dark:text-neutral-400">暂无可用指标</div>'
    
    def generate_chart_container(self, runs, metric, chart_type):
        """Generate chart container HTML"""
        chart_id = f"chart-{metric['name']}-{chart_type}"
        
        return f"""
        <div class="chart-container">
            <div class="chart-header">
                <h4 class="chart-title">{metric['display_name']} ({metric['unit']})</h4>
                <span class="chart-type">{chart_type == 'line' and '折线图' or '柱状图'}</span>
            </div>
            <div class="chart-canvas-container">
                <canvas id="{chart_id}"></canvas>
            </div>
            <p class="chart-description">{metric['description']}</p>
        </div>
        """
    
    def generate_chart_scripts(self):
        """Generate JavaScript for all charts"""
        scripts = []
        
        for tool_name, tool_data in self.test_data.items():
            # Select key metrics for charts
            key_metrics = []
            priority_metrics = ['TTFT', 'Throughput', 'accuracy', 'f1_score']
            
            # Add priority metrics first
            for metric_name in priority_metrics:
                for metric in tool_data['metrics_schema']:
                    if metric['name'] == metric_name and len(key_metrics) < 2:
                        key_metrics.append(metric)
            
            # Fill with other metrics if needed
            for metric in tool_data['metrics_schema']:
                if len(key_metrics) >= 2:
                    break
                if not any(m['name'] == metric['name'] for m in key_metrics):
                    key_metrics.append(metric)
            
            # Generate scripts for selected metrics
            for metric in key_metrics:
                chart_type = metric.get('default_chart_type')
                if chart_type in ['line', 'bar']:
                    script = self.generate_chart_script(
                        tool_data['runs'], 
                        metric, 
                        chart_type
                    )
                    scripts.append(script)
        
        return '\n'.join(scripts)
    
    def generate_chart_script(self, runs, metric, chart_type):
        """Generate JavaScript for a specific chart"""
        chart_id = f"chart-{metric['name']}-{chart_type}"
        
        # Prepare data
        labels = []
        values = []
        
        for run in sorted(runs, key=lambda x: x['timestamp']):
            labels.append(run['build_id'])
            values.append(run['metrics'].get(metric['name'], 0))
        
        # Chart configuration
        if chart_type == 'line':
            config = f"""
                new Chart(document.getElementById('{chart_id}'), {{
                    type: 'line',
                    data: {{
                        labels: {json.dumps(labels)},
                        datasets: [{{
                            label: '{metric['display_name']}',
                            data: {json.dumps(values)},
                            borderColor: '#2dae7d',
                            backgroundColor: 'rgba(45, 174, 125, 0.1)',
                            tension: 0.2,
                            fill: false,
                            pointRadius: 3,
                            pointHoverRadius: 5
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                display: false
                            }},
                            tooltip: {{
                                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                titleFont: {{
                                    size: 12
                                }},
                                bodyFont: {{
                                    size: 11
                                }}
                            }}
                        }},
                        scales: {{
                            y: {{
                                beginAtZero: {'true' if metric.get('lower_is_better', False) else 'false'},
                                grid: {{
                                    color: 'rgba(0, 0, 0, 0.05)'
                                }},
                                ticks: {{
                                    font: {{
                                        size: 10
                                    }}
                                }}
                            }},
                            x: {{
                                grid: {{
                                    display: false
                                }},
                                ticks: {{
                                    font: {{
                                        size: 10
                                    }},
                                    maxRotation: 45,
                                    minRotation: 45
                                }}
                            }}
                        }},
                        interaction: {{
                            mode: 'index',
                            intersect: false
                        }}
                    }}
                }});
            """
        else:  # bar chart
            config = f"""
                new Chart(document.getElementById('{chart_id}'), {{
                    type: 'bar',
                    data: {{
                        labels: {json.dumps(labels)},
                        datasets: [{{
                            label: '{metric['display_name']}',
                            data: {json.dumps(values)},
                            backgroundColor: 'rgba(45, 174, 125, 0.7)',
                            borderColor: '#2dae7d',
                            borderWidth: 1,
                            borderRadius: 4
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                display: false
                            }},
                            tooltip: {{
                                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                titleFont: {{
                                    size: 12
                                }},
                                bodyFont: {{
                                    size: 11
                                }}
                            }}
                        }},
                        scales: {{
                            y: {{
                                beginAtZero: {'true' if metric.get('lower_is_better', False) else 'false'},
                                grid: {{
                                    color: 'rgba(0, 0, 0, 0.05)'
                                }},
                                ticks: {{
                                    font: {{
                                        size: 10
                                    }}
                                }}
                            }},
                            x: {{
                                grid: {{
                                    display: false
                                }},
                                ticks: {{
                                    font: {{
                                        size: 10
                                    }},
                                    maxRotation: 45,
                                    minRotation: 45
                                }}
                            }}
                        }}
                    }}
                }});
            """
        
        return f"document.addEventListener('DOMContentLoaded', function() {{ {config} }});"


def main():
    """Main function to generate the demo report"""
    generator = LLMReportGenerator()
    output_file = generator.generate_html_report()
    
    print(f"\n✅ LLM测试报告Demo生成成功！")
    print(f"📁 输出文件: {output_file}")
    print(f"🌐 在浏览器中打开文件以查看交互式图表")
    print(f"\n报告包含:")
    print(f"  • 性能指标 (TTFT, TPOT, 吞吐量)")
    print(f"  • 准确性指标 (准确率, F1分数)")
    print(f"  • 交互式折线图和柱状图")
    print(f"  • 构建版本对比")
    print(f"  • 响应式设计，支持移动端查看")


if __name__ == "__main__":
    main()