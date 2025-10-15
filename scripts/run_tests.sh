#!/bin/bash
# Test execution script for CI/CD pipeline

set -e

echo "===== Starting Test Execution ====="
echo "Timestamp: $(date)"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 创建必要的目录
echo "Creating directories..."
mkdir -p tests/reports allure-results logs

# 启动服务
echo "Starting test environment..."
docker-compose -f docker-compose.test.yml up -d

echo "Waiting for service to be ready..."
timeout=300
interval=5
elapsed=0

while [ $elapsed -lt $timeout ]; do
    if curl -f http://localhost:5000/health >/dev/null 2>&1; then
        echo -e "${GREEN}Service is ready!${NC}"
        break
    fi
    echo "Waiting for service... ($elapsed/$timeout seconds)"
    sleep $interval
    elapsed=$((elapsed + interval))
done

if [ $elapsed -ge $timeout ]; then
    echo -e "${RED}Service failed to start within timeout period${NC}"
    docker-compose -f docker-compose.test.yml logs
    exit 1
fi

# 运行测试
echo "Running tests..."
test_start_time=$(date +%s)

if docker-compose -f docker-compose.test.yml run --rm test pytest; then
    echo -e "${GREEN}All tests passed!${NC}"
    test_result=0
else
    echo -e "${RED}Some tests failed!${NC}"
    test_result=1
fi

test_end_time=$(date +%s)
test_duration=$((test_end_time - test_start_time))

echo "Test execution time: ${test_duration} seconds"

# 生成Allure报告
echo "Generating Allure report..."
if command -v allure >/dev/null 2>&1; then
    allure generate allure-results -o allure-report --clean
    echo -e "${GREEN}Allure report generated${NC}"
else
    echo -e "${YELLOW}Allure command not found, skipping report generation${NC}"
fi

# 生成PDF报告
echo "Generating PDF report..."
if python scripts/generate_pdf_report.py; then
    echo -e "${GREEN}PDF report generated${NC}"
else
    echo -e "${YELLOW}PDF report generation failed${NC}"
fi

# 显示测试摘要
echo "===== Test Summary ====="
echo "Test Duration: ${test_duration} seconds"
echo "HTML Report: tests/reports/test_report.html"
echo "Allure Results: allure-results/"
echo "PDF Report: tests/reports/test_report.pdf"

# 清理
echo "Cleaning up..."
docker-compose -f docker-compose.test.yml down -v

echo -e "${GREEN}Test execution completed!${NC}"
exit $test_result