# Jenkins CI/CD 操作手册

## 项目概述

这是一个完整的Jenkins CI/CD演示项目，包含：
- Flask Web服务
- 完整的测试套件
- Docker容器化部署
- Allure和PDF报告生成
- 邮件通知系统

## 环境准备

### 1. 系统要求
- Docker 和 Docker Compose
- Jenkins（带Pipeline、Docker Pipeline、Allure、Email插件）
- Python 3.8+

### 2. Jenkins插件安装
```bash
# 在Jenkins中安装以下插件：
- Pipeline
- Docker Pipeline Plugin
- Allure Jenkins Plugin
- Email Extension Plugin
- Docker Commons Plugin
- HTML Publisher Plugin
```

### 3. 镜像源优化配置（推荐）
在阿里云环境下，建议配置镜像源以加速构建：

#### Docker镜像构建优化
项目已配置阿里云镜像源：
- **APT源**: 使用阿里云Debian镜像源加速系统包下载
- **PyPI源**: 使用阿里云PyPI镜像源加速Python包下载

#### 手动配置PyPI源（可选）
如果需要在其他环境使用阿里云源：
```bash
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip config set install.trusted-host mirrors.aliyun.com
```

### 4. Docker Registry配置（可选）
如果需要推送镜像，配置Docker Registry：
```bash
# 启动本地Registry（可选）
docker run -d -p 5000:5000 --name registry registry:2
```

## Jenkins流水线配置

### 1. 创建Jenkins Job
- 选择 "Pipeline" 项目类型
- 配置源码管理为Git，URL: `https://github.com/Potterluo/jinkins-ci-demo.git`
- 在Pipeline配置中选择 "Pipeline script from SCM"
- SCM选择 "Git"
- 脚本路径: `Jenkinsfile`

### 2. Allure报告配置
在Jenkins全局工具配置中：
- 安装Allure Commandline（如果尚未安装）
- 进入"Manage Jenkins" → "Global Tool Configuration"
- 找到"Allure Commandline"，点击新增安装
- 选择合适的版本（推荐2.24+）

### 4. 环境变量配置
在Jenkins Job中配置以下环境变量：
```bash
DOCKER_REGISTRY=127.0.0.1:5000  # Docker Registry地址
REPO_URL=https://github.com/Potterluo/jinkins-ci-demo.git  # 仓库地址
EMAIL_RECIPIENTS=your-email@example.com  # 邮件通知接收者
DOCKER_HUB_USER=your_dockerhub_username  # Docker Hub用户名（可选）
DOCKER_HUB_TOKEN=your_dockerhub_token  # Docker Hub访问令牌（可选）
```

## 流水线阶段说明

### 1. PR验证 (PR Verification)
- 触发条件：PR-* 分支或手动选择 `PR_VERIFY`
- 功能：运行基本测试验证PR变更

### 2. 日常构建 (Daily Build & Smoke Test)
- 触发条件：定时触发或手动选择 `DAILY_BUILD`
- 功能：构建镜像并运行冒烟测试

### 3. 全量测试 (Full Test)
- 触发条件：手动选择 `FULL_TEST`
- 功能：运行完整的测试套件

### 4. 报告汇总
- 触发条件：所有阶段完成后自动执行
- 功能：收集并发布测试报告
- 输出：HTML报告和Allure报告
- 访问方式：Jenkins构建页面 → Allure Report链接

## CI/CD流水线使用指南

### 手动触发构建
1. 进入Jenkins项目页面
2. 点击"Build with Parameters"
3. 选择构建类型：
   - `PR_VERIFY`: PR验证模式
   - `DAILY_BUILD`: 日常构建模式
   - `FULL_TEST`: 全量测试模式
4. 选择是否发送邮件通知
5. 点击"Build"开始构建

### 查看测试报告
构建完成后，可通过以下方式查看报告：
1. **HTML报告**: 构建页面 → Test Report
2. **Allure报告**: 构建页面 → Allure Report（推荐，功能更丰富）

### 报告特点
- **HTML报告**: 轻量级，加载快，基本功能
- **Allure报告**:
  - 交互式界面
  - 测试历史趋势
  - 详细失败分析
  - 测试用例分类
  - 执行时间统计

## 本地开发和测试

### 1. 本地运行服务
```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py

# 测试接口
curl http://localhost:5000/hello
curl http://localhost:5000/health
```

### 2. 本地运行测试

#### Windows环境
```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试（基本方式）
python -m pytest tests/test_app.py -v

# 运行测试并生成HTML报告
python -m pytest tests/test_app.py --html=tests/reports/test_report.html --self-contained-html

# 运行测试并生成Allure报告
python -m pytest tests/test_app.py --alluredir=tests/reports/allure-results

# 查看Allure报告（需要先安装Allure Commandline）
allure generate tests/reports/allure-results -o tests/reports/allure-report --clean
allure open tests/reports/allure-report
```

**Windows特殊说明：**
- 如果遇到测试导入问题，使用模块方式运行：`python -m pytest`
- 确保已创建报告目录：`mkdir tests\reports 2>nul`
- Allure需要单独安装：从 https://github.com/allure-framework/allure2/releases 下载

#### Linux/macOS环境
```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
python -m pytest tests/test_app.py -v

# 运行测试并生成HTML报告
python -m pytest tests/test_app.py --html=tests/reports/test_report.html --self-contained-html

# 运行测试并生成Allure报告
python -m pytest tests/test_app.py --alluredir=tests/reports/allure-results

# 查看Allure报告
allure generate tests/reports/allure-results -o tests/reports/allure-report --clean
allure open tests/reports/allure-report
```

**注意：** 在Windows上直接运行Flask应用和测试时可能遇到环境问题。在实际CI/CD环境中，测试将在Docker容器中运行，不会遇到此问题。

### 3. Docker环境测试（推荐用于完整测试流程）
```bash
# 方法2：使用Docker Compose（与CI/CD环境一致）
docker-compose -f docker-compose.test.yml up --build

# 方法3：使用测试脚本
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

### 4. 生成报告

#### Windows环境
```cmd
REM 创建报告目录
if not exist tests\reports mkdir tests\reports

REM 生成HTML报告
python -m pytest --html=tests\reports\test_report.html --self-contained-html

REM 生成Allure报告
python -m pytest --alluredir=tests\reports\allure-results

REM 生成并查看Allure报告（需要Allure Commandline）
allure generate tests\reports\allure-results -o tests\reports\allure-report --clean
allure open tests\reports\allure-report

REM 生成PDF报告
python scripts\generate_pdf_report.py
```

#### Linux/macOS环境
```bash
# 创建报告目录
mkdir -p tests/reports

# 生成HTML报告
pytest --html=tests/reports/test_report.html --self-contained-html

# 生成Allure报告
pytest --alluredir=tests/reports/allure-results

# 生成并查看Allure报告
allure generate tests/reports/allure-results -o tests/reports/allure-report --clean
allure open tests/reports/allure-report

# 生成PDF报告
python scripts/generate_pdf_report.py
```

#### 报告类型说明
- **HTML报告**: 简单的网页测试报告，适合快速查看结果
- **Allure报告**: 交互式测试报告，提供详细的测试分析和历史趋势
- **PDF报告**: 适合归档和分享的格式化报告

## 项目文件结构说明

```
.
├── app.py                    # Flask应用主文件
├── Dockerfile               # 应用Docker镜像构建文件
├── Dockerfile.test          # 测试环境Docker镜像构建文件
├── docker-compose.test.yml  # 测试环境编排文件
├── Jenkinsfile             # Jenkins流水线配置
├── requirements.txt         # Python依赖
├── setup.py                # Python包配置
├── pytest.ini              # Pytest配置
├── README.md              # 项目说明
├── OPERATION_MANUAL.md    # 操作手册
├── scripts/
│   ├── generate_pdf_report.py  # PDF报告生成脚本
│   └── run_tests.sh       # 测试执行脚本
└── tests/
    └── test_app.py        # 测试用例
```

## 常见问题和解决方案

### 1. 镜像构建失败
- 检查Docker是否正常运行
- 确保Dockerfile语法正确
- 检查依赖包是否可访问

### 2. 测试环境启动失败
- 检查端口是否被占用
- 确保服务健康检查路径正确
- 查看Docker Compose日志

### 3. Allure报告无法生成
- 确保Jenkins安装了Allure插件
- 检查allure-results目录是否存在
- 确认pytest-allure-adaptor版本兼容

### 4. PDF报告生成失败
- 确保requirements.txt中包含weasyprint
- 检查HTML报告文件是否存在
- 验证系统字体配置

## 扩展和自定义

### 1. 添加更多测试
在`tests/`目录下创建新的测试文件，遵循`test_*.py`命名规范。

### 2. 自定义报告模板
修改`scripts/generate_pdf_report.py`中的CSS样式来自定义PDF报告外观。

### 3. 配置邮件模板
在Jenkins的邮件扩展插件中自定义邮件模板，添加更多构建信息。

## 安全注意事项

1. 不要在代码中硬编码敏感信息
2. 使用Jenkins凭据存储Docker Hub令牌
3. 定期更新依赖包以修复安全漏洞
4. 限制Docker容器的权限

## 性能优化建议

1. 使用Jenkins节点进行并行构建
2. 配置Docker镜像缓存
3. 优化测试执行顺序
4. 使用增量构建策略

## 故障排除

### 查看Jenkins构建日志
在Jenkins构建页面查看详细日志信息。

### 本地调试
```bash
# 运行测试环境
docker-compose -f docker-compose.test.yml up -d
docker-compose -f docker-compose.test.yml logs -f

# 运行单个测试
docker-compose -f docker-compose.test.yml run --rm test pytest tests/test_app.py::TestHelloWorldService::test_hello_world
```

### 清理资源
```bash
# 停止测试环境
docker-compose -f docker-compose.test.yml down -v

# 清理Docker构建缓存
docker system prune -f
```

## 版本控制和部署

1. 使用Git标签管理版本
2. 在Jenkins中配置分支构建策略
3. 设置环境变量区分不同部署环境
4. 实施蓝绿部署或滚动更新策略