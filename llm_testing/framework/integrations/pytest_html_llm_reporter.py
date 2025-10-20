"""
pytest-html integration for LLM Test Framework
This module provides pytest hooks for integrating LLM test data into pytest-html reports
"""

from .. import llm_reporter, pytest_html_report_title, pytest_html_results_summary

__all__ = ['pytest_html_report_title', 'pytest_html_results_summary']