# Hello World Service - Jenkins CI/CD Demo

这是一个简单的 Flask 服务演示项目，展示了完整的 Jenkins CI/CD 流程，包括 Allure 报告集成、PDF 报告生成、LLM测试框架和邮件通知。

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
├── llm_testing/            # LLM测试框架
│   ├── data/               # LLM测试数据
│   ├── framework/          # LLM测试框架核心代码
│   ├── reports/            # LLM测试报告
│   ├── generate_llm_demo.py # LLM演示生成脚本
│   └── run_llm_demo.py     # LLM演示运行脚本
└── tests/
    └── test_app.py         # 测试用例
```

## 功能特性

- **简单服务**: GET /hello 返回 Hello World
- **健康检查**: GET /health 健康状态检查
- **完整测试**: Pytest + Allure + Docker 测试
- **CI/CD 集成**: Jenkins 流水线支持 PR、日常构建、全量测试
- **报告系统**: HTML、Allure、PDF 多格式报告
- **LLM 测试**: 集成AI模型性能与精度评测框架
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

### 4. 生成报告
```bash
# 生成 Allure 报告
allure generate allure-results -o allure-report --clean
allure open allure-report

# 生成 PDF 报告
python scripts/generate_pdf_report.py

# 生成 LLM 测试报告
cd llm_testing
python run_llm_demo.py
```

### LLM 测试框架

#### 核心功能

##### 📊 数据集成
- **多工具支持**: 支持AISBench、MMLU、LLMPerf等评测工具
- **JSON数据格式**: 标准化的数据结构和模式定义
- **动态数据加载**: 支持从JSON文件动态加载评测数据
- **与pytest解耦**: 独立运行，不依赖pytest框架

##### 📈 可视化展示
- **多种图表类型**: 表格、折线图、柱状图
- **交互式图表**: 使用Chart.js实现响应式交互图表
- **趋势分析**: 支持构建版本间的数据对比
- **响应式设计**: 适配桌面端和移动端

##### 🔧 配置灵活
- **指标配置**: 支持自定义指标模式（名称、单位、格式、图表类型）
- **样式定制**: 可自定义CSS样式和主题
- **独立运行**: 可作为独立工具使用

### 使用示例

#### 运行LLM演示
```bash
# 方法1: 运行演示脚本（兼容模式）
cd llm_testing
python run_llm_demo.py

# 方法2: 运行独立报告生成器（推荐）
cd llm_testing
python generate_standalone_report.py

# 生成报告位置: llm_testing/reports/llm_standalone_report.html
```

#### 添加新数据
1. 在 `llm_testing/data/` 目录下创建新的JSON文件
2. 遵循标准数据格式（参考现有示例文件）
3. 运行报告生成脚本

#### LLM数据格式
```json
{
  "tool": "工具名称",
  "description": "工具描述",
  "metrics_schema": [
    {
      "name": "指标名称",
      "display_name": "显示名称", 
      "unit": "单位",
      "description": "指标描述",
      "lower_is_better": true/false,
      "format": "{:.2f}",
      "default_chart_type": "bar/line"
    }
  ],
  "runs": [
    {
      "build_id": "构建ID",
      "timestamp": "时间戳",
      "env": {
        "model": "模型名称",
        "backend": "后端框架",
        "description": "环境描述"
      },
      "metrics": {
        "指标名称": 指标值
      }
    }
  ]
}
```

#### 独立使用LLM框架
```python
from llm_testing.framework.demo_generator import LLMReportGenerator

# 创建报告生成器
generator = LLMReportGenerator()

# 生成HTML报告
output_file = generator.generate_html_report("my_report.html")
print(f"报告已生成: {output_file}")
```

### 支持的评测工具

#### AISBench (性能基准测试)
- **TTFT**: Time to First Token (首token时间)
- **TPOT**: Time Per Output Token (每输出token时间)
- **Throughput**: 端到端吞吐率
- **Latency**: 延迟指标

#### MMLU (多任务语言理解)
- **Accuracy**: 整体准确率
- **F1 Score**: F1分数
- **STEM Accuracy**: STEM领域准确率
- **Humanities Accuracy**: 人文学科准确率

#### LLMPerf (综合性能测试)
- **Average Latency**: 平均延迟
- **P50/P95 Latency**: 百分位延迟
- **Tokens per Second**: token生成速率
- **Requests per Second**: 请求处理速率

## Jenkins 配置

### 必要插件
- Pipeline
- Docker Pipeline
- Allure Jenkins Plugin
- Email Extension Plugin
- HTML Publisher Plugin

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

### 4. LLM 测试报告
- 位置: `llm_testing/reports/llm_test_report_demo.html`
- 包含: AI模型性能与精度数据的可视化展示

## Jenkins CI集成

### 配置要求
1. 安装必要的Jenkins插件：
   - Pipeline Plugin
   - Docker Pipeline Plugin
   - HTML Publisher Plugin

2. 确保Jenkins节点有以下依赖：
   - Python 3.8+
   - pip包管理器

### Jenkinsfile配置示例
```groovy
pipeline {
    agent any
    
    environment {
        EMAIL_RECIPIENTS = "team@example.com"
    }
    
    stages {
        // 构建和测试阶段
        stage('Build and Test') {
            steps {
                script {
                    // 构建应用镜像
                    sh 'docker build -t hello-world-service .'
                    
                    // 运行应用测试
                    sh 'docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit'
                }
            }
        }
        
        // LLM测试阶段（已与pytest解耦）
        stage('LLM Tests') {
            steps {
                script {
                    echo "===== Starting LLM Tests ====="
                    
                    // 运行独立的LLM报告生成器
                    sh 'cd llm_testing && python generate_standalone_report.py'
                }
            }
            post {
                success {
                    echo "LLM Tests completed successfully"
                }
                failure {
                    echo "LLM Tests failed"
                    currentBuild.result = 'FAILURE'
                }
            }
        }
        
        // 报告发布阶段
        stage('Publish Reports') {
            steps {
                script {
                    // 发布标准测试报告
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'tests/reports',
                        reportFiles: 'test_report.html',
                        reportName: 'Test Report'
                    ])
                    
                    // 发布Allure报告
                    script {
                        try {
                            allure([
                                includeProperties: false,
                                jdk: '',
                                properties: [],
                                reportBuildPolicy: 'ALWAYS',
                                results: [[path: 'tests/reports/allure-results']]
                            ])
                        } catch (Exception e) {
                            echo "Allure report generation failed: ${e.getMessage()}"
                        }
                    }
                    
                    // 发布LLM测试报告（独立版本）
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'llm_testing/reports',
                        reportFiles: 'llm_standalone_report.html',
                        reportName: 'LLM Test Report'
                    ])
                }
            }
        }
    }
    
    post {
        always {
            // 清理资源
            sh 'docker-compose -f docker-compose.test.yml down -v || true'
            sh 'docker system prune -f || true'
        }
        
        // 发送邮件通知
        success {
            emailext(
                subject: "[Jenkins] Build SUCCESS - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: '''
                <html>
                <body>
                    <h2>Build Successful</h2>
                    <p><strong>Project:</strong> ${env.JOB_NAME}</p>
                    <p><strong>Build Number:</strong> #${env.BUILD_NUMBER}</p>
                    <p><strong>Status:</strong> SUCCESS</p>
                    <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p><strong>Reports:</strong></p>
                    <ul>
                        <li><a href="${env.BUILD_URL}Test_Report/">Test Report</a></li>
                        <li><a href="${env.BUILD_URL}Allure_Report/">Allure Report</a></li>
                        <li><a href="${env.BUILD_URL}LLM_Test_Report/">LLM Test Report</a></li>
                    </ul>
                </body>
                </html>
                ''',
                to: "${EMAIL_RECIPIENTS}",
                mimeType: 'text/html'
            )
        }
        
        failure {
            emailext(
                subject: "[Jenkins] Build FAILED - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: '''
                <html>
                <body>
                    <h2>Build Failed</h2>
                    <p><strong>Project:</strong> ${env.JOB_NAME}</p>
                    <p><strong>Build Number:</strong> #${env.BUILD_NUMBER}</p>
                    <p><strong>Status:</strong> FAILED</p>
                    <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p>Please check the build logs for details.</p>
                </body>
                </html>
                ''',
                to: "${EMAIL_RECIPIENTS}",
                mimeType: 'text/html'
            )
        }
    }
}
```

### 集成要点

1. **LLM测试执行**：
   - LLM框架已与pytest完全解耦
   - 通过 `generate_standalone_report.py` 独立生成报告
   - 不再依赖pytest测试框架

2. **报告发布**：
   - LLM Test Report: 独立的交互式报告
   - 报告完全自包含，无需外部依赖

3. **数据收集**：
   - 在CI环境中，可以通过脚本收集实际的LLM测试数据
   - 将JSON数据文件放置在 `llm_testing/data/` 目录中

4. **扩展建议**：
   - 配置定时任务定期运行LLM基准测试
   - 集成性能回归检测机制
   - 添加历史数据对比功能
```

## 邮件通知

构建完成后自动发送邮件通知，包含：
- 构建状态（成功/失败）
- 测试摘要
- Allure 报告链接
- PDF 报告附件
- LLM 测试报告

## 扩展建议

1. **测试覆盖**: 添加更多测试用例和边界条件
2. **性能测试**: 集成性能测试工具
3. **LLM测试**: 扩展AI模型评测能力
4. **安全扫描**: 添加安全漏洞扫描
5. **多环境**: 支持开发、测试、生产环境
6. **回滚机制**: 添加自动回滚功能