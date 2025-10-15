# Hello World Service - Jenkins CI/CD Demo

这是一个简单的 Flask 服务演示项目，展示了完整的 Jenkins CI/CD 流程，包括 Allure 报告集成、PDF 报告生成和邮件通知。

## 项目结构

```
.
├── app.py                    # Flask 服务主文件
├── requirements.txt          # Python 依赖
├── Dockerfile               # 服务镜像构建文件
├── Dockerfile.test          # 测试镜像构建文件
├── docker-compose.test.yml  # 测试环境编排
├── pytest.ini              # Pytest 配置
├── setup.py                # Python 包配置
├── Jenkinsfile             # Jenkins 流水线配置
├── scripts/
│   ├── run_tests.sh        # 测试执行脚本
│   └── generate_pdf_report.py  # PDF 报告生成脚本
└── tests/
    └── test_app.py         # 测试用例
```

## 功能特性

- **简单服务**: GET /hello 返回 Hello World
- **健康检查**: GET /health 健康状态检查
- **完整测试**: Pytest + Allure + Docker 测试
- **CI/CD 集成**: Jenkins 流水线支持 PR、日常构建、全量测试
- **报告系统**: HTML、Allure、PDF 多格式报告
- **通知机制**: 邮件通知和附件发送

## 本地测试

### 1. 运行服务
```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py

# 测试接口
curl http://localhost:5000/hello
curl http://localhost:5000/health
```

### 2. 验证应用功能
```bash
# 快速验证应用功能
python verify_app.py
```

### 3. 运行测试
```bash
# 方法1：使用pytest直接运行（适用于开发环境）
pip install -r requirements.txt
python -m pytest tests/test_app.py -v

# 方法2：使用Docker Compose（与CI/CD环境一致）
docker-compose -f docker-compose.test.yml up --build

# 方法3：使用测试脚本
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

### 3. 生成报告
```bash
# 生成 Allure 报告
allure generate allure-results -o allure-report --clean
allure open allure-report

# 生成 PDF 报告
python scripts/generate_pdf_report.py
```

## Jenkins 配置

### 必要插件
- Pipeline
- Docker Pipeline
- Allure Jenkins Plugin
- Email Extension Plugin

### 环境变量
```bash
DOCKER_REGISTRY=127.0.0.1:5000
REPO_URL=https://github.com/your-repo/hello-world-service.git
EMAIL_RECIPIENTS=team@company.com,dev@company.com
```

### 构建类型
1. **PR Verification**: PR 触发或手动选择 `PR_VERIFY`
2. **Daily Build**: 定时触发或手动选择 `DAILY_BUILD`
3. **Full Test**: 手动选择 `FULL_TEST`

## 报告说明

### 1. HTML 报告
- 位置: `tests/reports/test_report.html`
- 包含: 测试用例、执行时间、结果统计

### 2. Allure 报告
- 位置: Jenkins 构建页面 Allure 标签
- 包含: 详细测试步骤、趋势分析、历史记录

### 3. PDF 报告
- 位置: `tests/reports/test_report.pdf`
- 包含: 测试摘要、结果详情、邮件附件

## 邮件通知

构建完成后自动发送邮件通知，包含：
- 构建状态（成功/失败）
- 测试摘要
- Allure 报告链接
- PDF 报告附件

## 扩展建议

1. **测试覆盖**: 添加更多测试用例和边界条件
2. **性能测试**: 集成性能测试工具
3. **安全扫描**: 添加安全漏洞扫描
4. **多环境**: 支持开发、测试、生产环境
5. **回滚机制**: 添加自动回滚功能