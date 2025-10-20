"""
LLM Test Framework - pytest-html integration plugin
Extends pytest-html to display LLM benchmark data with charts and tables
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import pytest


class LLMTestData:
    """Manages LLM test data from JSON files"""
    
    def __init__(self, data_dir: str = "../llm_testing/data"):
        self.data_dir = Path(data_dir)
        self.test_data: Dict[str, Dict] = {}
        self.load_all_data()
    
    def load_all_data(self):
        """Load all JSON files from the data directory"""
        if not self.data_dir.exists():
            return
        
        for json_file in self.data_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    tool_name = data.get('tool', json_file.stem)
                    self.test_data[tool_name] = data
            except Exception as e:
                print(f"Warning: Could not load {json_file}: {e}")
    
    def get_tools(self) -> List[str]:
        """Get list of available tools"""
        return list(self.test_data.keys())
    
    def get_tool_data(self, tool_name: str) -> Optional[Dict]:
        """Get data for a specific tool"""
        return self.test_data.get(tool_name)


class ChartRenderer:
    """Renders charts for LLM metrics"""
    
    @staticmethod
    def render_table(metrics_data: List[Dict], metric_schema: List[Dict]) -> str:
        """Render metrics as a table"""
        if not metrics_data:
            return '<div class="no-data">No data available</div>'
        
        # Create table header
        headers = ['Build ID', 'Timestamp', 'Environment']
        for metric in metric_schema:
            headers.append(f"{metric['display_name']} ({metric['unit']})")
        
        # Create table HTML
        html_content = '<table class="llm-metrics-table">'
        html_content += '<thead><tr>'
        for header in headers:
            html_content += f'<th>{header}</th>'
        html_content += '</tr></thead>'
        
        # Create table rows
        html_content += '<tbody>'
        for run in metrics_data:
            html_content += '<tr>'
            html_content += f'<td>{run["build_id"]}</td>'
            html_content += f'<td>{run["timestamp"][:10]}</td>'
            html_content += f'<td>{run["env"].get("description", "N/A")}</td>'
            
            for metric in metric_schema:
                metric_name = metric['name']
                value = run['metrics'].get(metric_name, 'N/A')
                if value != 'N/A':
                    formatted_value = metric['format'].format(value)
                    html_content += f'<td>{formatted_value}</td>'
                else:
                    html_content += '<td>N/A</td>'
            
            html_content += '</tr>'
        
        html_content += '</tbody></table>'
        return html_content
    
    @staticmethod
    def render_line_chart(metrics_data: List[Dict], metric_schema: List[Dict], metric_name: str) -> str:
        """Render a line chart for a specific metric"""
        if not metrics_data:
            return '<div class="no-data">No data available</div>'
        
        # Find the metric schema
        metric_info = next((m for m in metric_schema if m['name'] == metric_name), None)
        if not metric_info:
            return f'<div class="error">Metric {metric_name} not found</div>'
        
        # Prepare data for chart
        labels = []
        values = []
        
        for run in sorted(metrics_data, key=lambda x: x['timestamp']):
            labels.append(run['build_id'])
            values.append(run['metrics'].get(metric_name, 0))
        
        # Create chart container
        chart_id = f"chart-{metric_name}"
        chart_data = {
            'labels': labels,
            'datasets': [{
                'label': metric_info['display_name'],
                'data': values,
                'borderColor': 'rgb(75, 192, 192)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'tension': 0.1
            }]
        }
        
        chart_html = f"""
        <div class="llm-chart-container">
            <h4>{metric_info['display_name']} ({metric_info['unit']})</h4>
            <canvas id="{chart_id}" width="400" height="200"></canvas>
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    const ctx = document.getElementById('{chart_id}').getContext('2d');
                    new Chart(ctx, {{
                        type: 'line',
                        data: {json.dumps(chart_data)},
                        options: {{
                            responsive: true,
                            plugins: {{
                                title: {{
                                    display: true,
                                    text: '{metric_info['description']}'
                                }}
                            }},
                            scales: {{
                                y: {{
                                    beginAtZero: false,
                                    title: {{
                                        display: true,
                                        text: '{metric_info['unit']}'
                                    }}
                                }},
                                x: {{
                                    title: {{
                                        display: true,
                                        text: 'Build ID'
                                    }}
                                }}
                            }}
                        }}
                    }});
                }});
            </script>
        </div>
        """
        
        return chart_html
    
    @staticmethod
    def render_bar_chart(metrics_data: List[Dict], metric_schema: List[Dict], metric_name: str) -> str:
        """Render a bar chart for a specific metric"""
        if not metrics_data:
            return '<div class="no-data">No data available</div>'
        
        # Find the metric schema
        metric_info = next((m for m in metric_schema if m['name'] == metric_name), None)
        if not metric_info:
            return f'<div class="error">Metric {metric_name} not found</div>'
        
        # Prepare data for chart
        labels = []
        values = []
        colors = ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 205, 86, 0.2)']
        border_colors = ['rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 205, 86)']
        
        for i, run in enumerate(sorted(metrics_data, key=lambda x: x['timestamp'])):
            labels.append(run['build_id'])
            values.append(run['metrics'].get(metric_name, 0))
        
        # Create chart container
        chart_id = f"bar-chart-{metric_name}"
        chart_data = {
            'labels': labels,
            'datasets': [{
                'label': metric_info['display_name'],
                'data': values,
                'backgroundColor': colors[:len(values)],
                'borderColor': border_colors[:len(values)],
                'borderWidth': 1
            }]
        }
        
        chart_html = f"""
        <div class="llm-chart-container">
            <h4>{metric_info['display_name']} ({metric_info['unit']})</h4>
            <canvas id="{chart_id}" width="400" height="200"></canvas>
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    const ctx = document.getElementById('{chart_id}').getContext('2d');
                    new Chart(ctx, {{
                        type: 'bar',
                        data: {json.dumps(chart_data)},
                        options: {{
                            responsive: true,
                            plugins: {{
                                title: {{
                                    display: true,
                                    text: '{metric_info['description']}'
                                }}
                            }},
                            scales: {{
                                y: {{
                                    beginAtZero: true,
                                    title: {{
                                        display: true,
                                        text: '{metric_info['unit']}'
                                    }}
                                }},
                                x: {{
                                    title: {{
                                        display: true,
                                        text: 'Build ID'
                                    }}
                                }}
                            }}
                        }}
                    }});
                }});
            </script>
        </div>
        """
        
        return chart_html


class LLMTestReporter:
    """Main reporter class for LLM test data"""
    
    def __init__(self):
        self.data_manager = LLMTestData()
        self.chart_renderer = ChartRenderer()
    
    def generate_report_section(self) -> str:
        """Generate the LLM test report section"""
        tools = self.data_manager.get_tools()
        
        if not tools:
            return '<div class="no-data">No LLM test data available</div>'
        
        sections = []
        
        for tool_name in tools:
            tool_data = self.data_manager.get_tool_data(tool_name)
            if not tool_data:
                continue
            
            # Tool header
            sections.append(f'<h2 class="llm-tool-title">{tool_data["tool"]} - {tool_data["description"]}</h2>')
            
            # Summary table
            sections.append('<h3>Summary Metrics</h3>')
            sections.append(self.chart_renderer.render_table(
                tool_data['runs'], 
                tool_data['metrics_schema']
            ))
            
            # Individual metric charts
            sections.append('<h3>Metric Trends</h3>')
            
            # Group charts by type
            line_charts = []
            bar_charts = []
            
            for metric in tool_data['metrics_schema']:
                metric_name = metric['name']
                chart_type = metric.get('default_chart_type')
                
                if chart_type == 'line':
                    line_charts.append(metric_name)
                elif chart_type == 'bar':
                    bar_charts.append(metric_name)
            
            # Render line charts
            if line_charts:
                sections.append('<h4>Trend Charts (Line)</h4>')
                for metric_name in line_charts:
                    sections.append(self.chart_renderer.render_line_chart(
                        tool_data['runs'],
                        tool_data['metrics_schema'],
                        metric_name
                    ))
            
            # Render bar charts
            if bar_charts:
                sections.append('<h4>Comparison Charts (Bar)</h4>')
                for metric_name in bar_charts:
                    sections.append(self.chart_renderer.render_bar_chart(
                        tool_data['runs'],
                        tool_data['metrics_schema'],
                        metric_name
                    ))
            
            sections.append('<hr>')
        
        return f'<div class="llm-test-report">{"".join(sections)}</div>'


# Global reporter instance
llm_reporter = LLMTestReporter()


def pytest_html_report_title(report):
    """Modify the report title"""
    report.title = "LLM Test Report"


def pytest_html_results_summary(prefix, summary, postfix):
    """Add LLM test data to the report summary"""
    # Add Chart.js library and styles
    chart_js_script = '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
    
    custom_styles = '''
    <style>
        .llm-test-report {
            margin: 20px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        .llm-test-report h2, .llm-tool-title {
            color: #333;
            border-bottom: 2px solid #007acc;
            padding-bottom: 10px;
        }
        .llm-test-report h3 {
            color: #555;
            margin-top: 20px;
        }
        .llm-test-report h4 {
            color: #666;
            margin-top: 15px;
        }
        .llm-metrics-table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            background: white;
        }
        .llm-metrics-table th, .llm-metrics-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        .llm-metrics-table th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        .llm-metrics-table tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .llm-chart-container {
            margin: 20px 0;
            padding: 15px;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            background-color: white;
        }
        .llm-chart-container h4 {
            margin-top: 0;
            color: #333;
        }
        .chart-wrapper {
            position: relative;
            height: 300px;
            margin: 20px 0;
        }
        .no-data {
            text-align: center;
            padding: 20px;
            color: #666;
            font-style: italic;
        }
        .error {
            color: #dc3545;
            padding: 10px;
            border: 1px solid #dc3545;
            border-radius: 4px;
            background-color: #f8d7da;
        }
    </style>
    '''
    
    prefix.append(chart_js_script)
    prefix.append(custom_styles)
    
    # Add LLM test report section
    try:
        llm_section = llm_reporter.generate_report_section()
        postfix.append('<h2>LLM Test Results</h2>')
        postfix.append(llm_section)
    except Exception as e:
        error_html = f'<div class="error">Error loading LLM test data: {e}</div>'
        postfix.append(error_html)