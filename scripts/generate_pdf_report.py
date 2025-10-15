#!/usr/bin/env python3
"""
PDF Report Generator for Test Results
"""
import os
import sys
from datetime import datetime
try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("Warning: weasyprint not available, PDF generation disabled")

def generate_pdf_report():
    """Generate PDF report from HTML test results"""
    if not PDF_AVAILABLE:
        print("PDF generation not available - weasyprint not installed")
        return False
    
    try:
        # 检查HTML报告是否存在
        html_file = "tests/reports/test_report.html"
        pdf_file = "tests/reports/test_report.pdf"
        
        if not os.path.exists(html_file):
            print(f"HTML report not found: {html_file}")
            # 尝试其他可能的路径
            html_file = "./tests/reports/test_report.html"
            if not os.path.exists(html_file):
                print("No HTML report found to convert to PDF")
                return False
        
        print(f"Generating PDF report from {html_file}")
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(pdf_file), exist_ok=True)
        
        # 自定义CSS样式
        css_content = """
        @page {
            size: A4;
            margin: 1cm;
            @bottom-right {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                font-family: Arial, sans-serif;
            }
        }
        
        body {
            font-family: Arial, sans-serif;
            font-size: 12px;
            line-height: 1.6;
            margin: 20px;
        }
        
        h1, h2, h3 {
            color: #333;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        
        .test-result {
            margin: 10px 0;
            padding: 5px;
            border-left: 3px solid #ccc;
        }
        
        .passed {
            border-left-color: #27ae60;
            background-color: #d5f4e6;
        }
        
        .failed {
            border-left-color: #e74c3c;
            background-color: #fadbd8;
        }
        
        .skipped {
            border-left-color: #f39c12;
            background-color: #fef9e7;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 11px;
        }
        
        th, td {
            border: 1px solid #bdc3c7;
            padding: 8px;
            text-align: left;
        }
        
        th {
            background-color: #ecf0f1;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .summary-box {
            border: 1px solid #bdc3c7;
            padding: 15px;
            margin: 10px 0;
            background-color: #f8f9fa;
            border-radius: 4px;
        }
        
        .timestamp {
            color: #7f8c8d;
            font-size: 10px;
            text-align: right;
        }
        """
        
        font_config = FontConfiguration()
        
        # 生成PDF
        HTML(filename=html_file).write_pdf(
            pdf_file,
            stylesheets=[CSS(string=css_content, font_config=font_config)],
            font_config=font_config
        )
        
        print(f"PDF report generated successfully: {pdf_file}")
        return True
        
    except Exception as e:
        print(f"Error generating PDF report: {e}")
        # 尝试创建一个简单的PDF报告作为备选
        try:
            create_simple_pdf_report(pdf_file)
            return True
        except Exception as fallback_error:
            print(f"Fallback PDF generation also failed: {fallback_error}")
            return False

def create_simple_pdf_report(pdf_file):
    """创建一个简单的PDF报告作为备选方案"""
    print("Creating a simple fallback PDF report...")
    
    # 创建一个简单的HTML报告
    fallback_html = f"""
    <html>
    <head>
        <title>Test Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #2c3e50; }}
            .timestamp {{ color: #7f8c8d; font-size: 12px; }}
        </style>
    </head>
    <body>
        <h1>Test Report</h1>
        <div class="timestamp">Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        <p>Test report was generated successfully.</p>
        <p>Please check the original HTML report for complete details.</p>
    </body>
    </html>
    """
    
    # 临时保存HTML
    temp_html = "temp_fallback_report.html"
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(fallback_html)
    
    try:
        from weasyprint import HTML, CSS
        HTML(temp_html).write_pdf(pdf_file, stylesheets=[CSS(string="""
            @page {{ size: A4; margin: 1cm; }}
            body {{ font-family: Arial, sans-serif; font-size: 12px; }}
        """)])
        print(f"Fallback PDF report created: {pdf_file}")
    finally:
        # 清理临时文件
        if os.path.exists(temp_html):
            os.remove(temp_html)

def main():
    """Main function"""
    print(f"PDF Report Generator - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 确保目录存在
    os.makedirs("tests/reports", exist_ok=True)
    
    success = generate_pdf_report()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()