#!/usr/bin/env python3
"""
LLM测试报告生成器
完全独立于pytest，仅通过JSON文件生成报告
"""

import sys
import os
import json
from pathlib import Path


def generate_standalone_report():
    """生成独立的LLM测试报告"""
    print("🚀 正在生成独立LLM测试报告...")
    
    try:
        # 添加当前目录和上级目录到Python路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        sys.path.insert(0, current_dir)
        sys.path.insert(0, parent_dir)
        
        # 导入报告生成器
        from llm_testing.framework.generator_html import LLMReportGenerator
        
        # 确保reports目录存在
        reports_dir = os.path.join(current_dir, 'reports')
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
            print(f"✅ 创建报告目录: {reports_dir}")
        
        # 生成报告
        generator = LLMReportGenerator("../llm_testing/data")
        output_file = generator.generate_html_report("reports/llm_eval_report.html")
        
        print(f"✅ 独立报告已生成: {output_file}")
        print(f"🌐 请用浏览器打开查看: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ 生成独立报告失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_data_files():
    """验证数据文件是否存在"""
    print("🔍 正在验证数据文件...")
    
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_dir):
        print(f"❌ 数据目录不存在: {data_dir}")
        return False
    
    # 检查目录中的所有JSON文件
    json_files = list(Path(data_dir).glob("*.json"))
    
    if not json_files:
        print("❌ 数据目录中没有找到JSON文件")
        return False
    
    print(f"✅ 找到 {len(json_files)} 个数据文件:")
    for file_path in json_files:
        print(f"  - {file_path.name}")
    
    return True


def show_report_info():
    """显示报告信息"""
    print("\n" + "=" * 60)
    print("📊 LLM测试报告信息")
    print("=" * 60)
    
    reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
    report_file = os.path.join(reports_dir, 'llm_standalone_report.html')
    
    if os.path.exists(report_file):
        print(f"✅ 报告已生成: {report_file}")
        print(f"   🌐 文件大小: {os.path.getsize(report_file)} 字节")
        print(f"   🕐 生成时间: {os.path.getctime(report_file)}")
    else:
        print("❌ 报告文件不存在")

def main():
    """主函数"""
    print("=" * 60)
    print("🤖 LLM测试报告生成器 (独立版本)")
    print("=" * 60)
    
    # 验证数据文件
    if not validate_data_files():
        print("❌ 数据文件验证失败，请检查 llm_testing/data/ 目录")
        return 1
    
    # 生成报告
    success = generate_standalone_report()
    
    # 显示报告信息
    show_report_info()
    
    if success:
        print("\n✅ 报告生成完成!")
        return 0
    else:
        print("\n❌ 报告生成失败!")
        return 1


if __name__ == "__main__":
    sys.exit(main())