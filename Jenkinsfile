// ======================================================================
// Jenkinsfile - Simplified for Basic CI/CD
// ======================================================================

pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = "127.0.0.1:5001"
        REPO_URL = "https://github.com/Potterluo/jinkins-ci-demo.git"
        REPORT_DIR = "tests/reports"
        EMAIL_RECIPIENTS = "duxiaolong22@mails.ucas.ac.cn"
    }

    parameters {
        string(name: 'MANUAL_BRANCH', defaultValue: 'main', description: '手动触发时需要构建的分支')
        choice(name: 'TRIGGER_TYPE', choices: ['PR_VERIFY', 'DAILY_BUILD', 'FULL_TEST'], description: '手动构建类型')
        booleanParam(name: 'SEND_EMAIL', defaultValue: true, description: '是否发送邮件通知')
    }

    triggers {
        // 每天 0 点触发一次
        cron('H 0 * * *')
    }

    stages {

        // =========================== PR 验证 =============================
        stage('PR Verification') {
            when {
                anyOf {
                    branch 'PR-*'
                    expression { params.TRIGGER_TYPE == 'PR_VERIFY' }
                }
            }
            steps {
                script {
                    echo "===== Starting PR Verification ====="
                    checkout scm

                    // 运行简单测试
                    runSimpleTest()
                }
            }
            post {
                always {
                    generateSimpleReports()
                    cleanupResources()
                }
                success {
                    sendNotification('PR Verification', 'SUCCESS')
                }
                failure {
                    sendNotification('PR Verification', 'FAILURE')
                }
            }
        }

        // ======================== 日构建 & 冒烟测试 =========================
        stage('Daily Build & Smoke Test') {
            when {
                anyOf {
                    triggeredBy 'TimerTrigger'
                    expression { params.TRIGGER_TYPE == 'DAILY_BUILD' }
                }
            }
            steps {
                script {
                    echo "===== Starting Daily Build & Smoke Test ====="
                    checkout([$class: 'GitSCM', branches: [[name: "*/main"]], userRemoteConfigs: [[url: "${REPO_URL}"]]])

                    // 构建镜像
                    buildSimpleImage("hello-world-service")

                    // 运行简单测试
                    runSimpleTest()
                }
            }
            post {
                always {
                    generateSimpleReports()
                    cleanupResources()
                }
                success {
                    sendNotification('Daily Build & Smoke Test', 'SUCCESS')
                }
                failure {
                    sendNotification('Daily Build & Smoke Test', 'FAILURE')
                }
            }
        }

        // ============================ 全量测试 ============================
        stage('Full Test') {
            when { expression { params.TRIGGER_TYPE == 'FULL_TEST' } }
            steps {
                script {
                    echo "===== Starting Full Test ====="
                    checkout([$class: 'GitSCM', branches: [[name: "*/main"]], userRemoteConfigs: [[url: "${REPO_URL}"]]])

                    // 构建镜像
                    buildSimpleImage("hello-world-service")

                    // 运行简单测试
                    runSimpleTest()
                }
            }
            post {
                always {
                    generateSimpleReports()
                    cleanupResources()
                }
                success {
                    sendNotification('Full Test', 'SUCCESS')
                }
                failure {
                    sendNotification('Full Test', 'FAILURE')
                }
            }
        }

        // ========================== LLM 测试 ============================
        stage('LLM Tests') {
            steps {
                script {
                    echo "===== Starting LLM Tests ====="
                    checkout scm

                    // 运行LLM框架测试
                    sh "cd llm_testing && python3 generate_report.py"
                }
            }
            post {
                success {
                    echo "LLM Tests completed successfully"
                }
                failure {
                    echo "LLM Tests failed"
                    script {
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }

        // ============================ 报告汇总 ============================
        stage('Collect Reports') {
            steps {
                script {
                    echo "Collecting all logs and reports..."
                    sh "mkdir -p ${REPORT_DIR}"

                    // 归档测试报告
                    archiveArtifacts artifacts: 'tests/reports/**', allowEmptyArchive: true

                    // 发布HTML报告
                    // publishHTML([
                    //     allowMissing: false,
                    //     alwaysLinkToLastBuild: true,
                    //     keepAll: true,
                    //     reportDir: 'tests/reports',
                    //     reportFiles: 'test_report.html',
                    //     reportName: 'Test Report',
                    //     reportTitles: 'Pytest Test Results'
                    // ])

                    // 发布Allure报告
                    script {
                        try {
                            // 简化的Allure报告配置
                            allure results: [[path: 'tests/reports/allure-results']]
                            echo "Allure report step completed"
                        } catch (Exception e) {
                            echo "Allure report generation failed: ${e.getMessage()}"
                            echo "This might be due to missing Allure Commandline in Jenkins"
                        }
                    }

                    // 发布LLM测试报告
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'llm_testing/reports',
                        reportFiles: 'llm_eval_report.html',
                        reportName: 'LLM Eval Report',
                        reportTitles: 'LLM Eval Results'
                    ])

                }
            }
        }
    }

    post {
        always {
            echo "Pipeline Finished: ${currentBuild.currentResult}"
            cleanWs()
        }
    }
}

// ======================================================================
// Functions (Outside pipeline)
// ==================================================================

// 构建简单镜像
def buildSimpleImage(imageName) {
    def fullImageName = "${env.DOCKER_REGISTRY}/${imageName}"
    def dateTag = "daily-${new Date().format('yyyyMMdd')}"
    def gitCommit = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()

    echo "Building Docker image: ${fullImageName}"

    // 构建Docker镜像
    sh """
    docker build -t ${fullImageName}:${dateTag} .
    docker tag ${fullImageName}:${dateTag} ${fullImageName}:${gitCommit}
    docker tag ${fullImageName}:${dateTag} ${fullImageName}:latest
    """
}

// 运行简单测试
def runSimpleTest() {
    echo "===== Running Simple Test Suite ====="

    try {
        // 检查当前目录和文件
        sh "ls -la"
        sh "pwd"

        // 修复可能的文件名大小写问题
        sh """
        if [ -f DockerFile ] && [ ! -f Dockerfile ]; then
            echo "Renaming DockerFile to Dockerfile for case sensitivity"
            mv DockerFile Dockerfile
        fi
        """

        sh "cat Dockerfile || echo 'Dockerfile not found'"

        // 检查Docker是否可用
        sh "docker --version"
        sh "docker-compose --version"

        // 构建和启动测试环境
        sh "docker-compose -f docker-compose.test.yml build"
        sh "docker-compose -f docker-compose.test.yml up -d"

        // 等待服务启动
        echo "Waiting for services to start..."
        sleep 1

        // 运行测试
        sh "docker-compose -f docker-compose.test.yml run --rm test pytest -v --html=tests/reports/test_report.html --alluredir=tests/reports/allure-results"

        // 检查Allure结果是否生成
        sh """
        echo '=== 检查Allure结果目录 ==='
        ls -la tests/reports/ || echo 'tests/reports目录不存在'
        ls -la tests/reports/allure-results/ || echo 'allure-results目录不存在'
        find tests/reports/allure-results/ -name '*.json' 2>/dev/null | head -5 || echo '没有找到JSON文件'
        echo '=== 检查完成 ==='
        """

    } catch (Exception e) {
            echo "Test execution failed: ${e.getMessage()}"

            // 显示Docker容器日志以便调试
            sh "docker-compose -f docker-compose.test.yml logs || true"

            script {
                currentBuild.result = 'FAILURE'
            }
            throw e
        }
}

// 生成简单报告
def generateSimpleReports() {
    echo "Generating test reports..."

    // 收集测试结果
    sh "mkdir -p ${REPORT_DIR}"

    // 简化的报告收集
    sh """
    echo '=== 收集测试报告 ==='
    ls -la tests/reports/ 2>/dev/null || echo 'No reports directory found'
    cp -r tests/reports/* ${REPORT_DIR}/ 2>/dev/null || echo 'No reports to copy'
    
    echo '=== 收集LLM测试报告 ==='
    ls -la llm_testing/reports/ 2>/dev/null || echo 'No LLM reports directory found'
    cp -r llm_testing/reports/* ${REPORT_DIR}/ 2>/dev/null || echo 'No LLM reports to copy'
    echo '=== 报告收集完成 ==='
    """
}

// 发送通知
def sendNotification(testType, status) {
    if (params.SEND_EMAIL) {
        echo "Sending email notification for ${testType} - ${status}"

        def subject = "[Jenkins] ${testType} - ${status} - ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        def body = """
        <html>
        <body>
            <h2>Jenkins Build Notification</h2>
            <p><strong>Project:</strong> ${env.JOB_NAME}</p>
            <p><strong>Build Number:</strong> #${env.BUILD_NUMBER}</p>
            <p><strong>Status:</strong> ${status}</p>
            <p><strong>Test Type:</strong> ${testType}</p>
            <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
            <p><strong>Test Report:</strong> <a href="${env.BUILD_URL}allure">Allure Report</a></p>

            <h3>Test Summary</h3>
            <p>Please check the attached reports and <a href="${env.BUILD_URL}allure">online test report</a> for detailed test results.</p>

            <p>Best regards,<br>Jenkins CI/CD System</p>
        </body>
        </html>
        """

        try {
            // 发送邮件，关键：添加 mailer 参数
            emailext(
                subject: subject,
                body: body,
                to: "${EMAIL_RECIPIENTS}",
                attachmentsPattern: 'tests/reports/*.pdf', // 注意：HTML文件可能无法作为附件正确发送，建议使用PDF
                mimeType: 'text/html',
            )
        } catch (Exception e) {
            echo "Failed to send email notification: ${e.getMessage()}"
        }
    }
}

// 清理资源
def cleanupResources() {
    echo "Cleaning up resources..."

    sh """
    # 停止并移除容器
    docker-compose -f docker-compose.test.yml down -v || true

    # 清理 dangling 镜像
    docker system prune -f || true
    """
}