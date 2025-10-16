#!/usr/bin/env python3
"""
调试Allure报告生成的脚本
"""
import os
import sys
import subprocess
import json

def check_allure_installation():
    """检查Allure是否已安装"""
    try:
        result = subprocess.run(['allure', '--version'],
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✓ Allure已安装: {result.stdout.strip()}")
            return True
        else:
            print("✗ Allure未安装或无法访问")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("✗ Allure未安装或不在PATH中")
        return False

def check_allure_results():
    """检查allure-results目录和文件"""
    results_dir = "tests/reports/allure-results"

    if not os.path.exists(results_dir):
        print(f"✗ 目录不存在: {results_dir}")
        return False

    print(f"✓ 目录存在: {results_dir}")

    # 列出所有文件
    files = os.listdir(results_dir)
    print(f"  文件数量: {len(files)}")

    if not files:
        print("✗ 目录为空")
        return False

    # 检查JSON文件
    json_files = [f for f in files if f.endswith('.json')]
    print(f"  JSON文件数量: {len(json_files)}")

    if not json_files:
        print("✗ 没有找到JSON文件")
        return False

    # 检查第一个JSON文件的内容
    try:
        with open(os.path.join(results_dir, json_files[0]), 'r') as f:
            data = json.load(f)
            print(f"  第一个JSON文件类型: {data.get('name', 'Unknown')}")
    except Exception as e:
        print(f"✗ 无法读取JSON文件: {e}")
        return False

    print("✓ Allure结果文件看起来正常")
    return True

def generate_allure_report():
    """生成Allure报告"""
    results_dir = "tests/reports/allure-results"
    report_dir = "tests/reports/allure-report"

    print("正在生成Allure报告...")

    cmd = [
        'allure', 'generate', results_dir,
        '-o', report_dir,
        '--clean'
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✓ Allure报告生成成功")
            print(f"  报告位置: {report_dir}")
            return True
        else:
            print(f"✗ Allure报告生成失败: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ Allure报告生成超时")
        return False
    except Exception as e:
        print(f"✗ Allure报告生成异常: {e}")
        return False

def main():
    print("=== Allure报告调试脚本 ===\n")

    # 1. 检查Allure安装
    print("1. 检查Allure安装:")
    allure_installed = check_allure_installation()
    print()

    # 2. 检查Allure结果文件
    print("2. 检查Allure结果文件:")
    results_ok = check_allure_results()
    print()

    # 3. 生成报告
    if allure_installed and results_ok:
        print("3. 生成Allure报告:")
        generate_allure_report()
        print()
    else:
        print("3. 跳过报告生成（前置条件未满足）")
        print()

if __name__ == "__main__":
    main()