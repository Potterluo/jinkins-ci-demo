// ======================================================================
// Jenkinsfile - Optimized with Allure Reports and Email Notifications
// ======================================================================

pipeline {
    agent any  // 使用任何可用的agent
    
    environment {
        DOCKER_REGISTRY = "127.0.0.1:5000"
        REPO_URL = "git@github.com:Potterluo/jinkins-ci-demo.git"
        REPORT_DIR = "tests/reports"
        ALLURE_DIR = "allure-results"
        EMAIL_RECIPIENTS = "2926612857@qq.com"
        DOCKER_HUB_USER = ""
        DOCKER_HUB_TOKEN = ""
    }

    parameters {
        string(name: 'MANUAL_BRANCH', defaultValue: 'main', description: '手动触发时需要构建的分支')
        choice(name: 'TRIGGER_TYPE', choices: ['PR_VERIFY', 'DAILY_BUILD', 'FULL_TEST'], description: '手动构建类型')
        booleanParam(name: 'SEND_EMAIL', defaultValue: true, description: '是否发送邮件通知')
        booleanParam(name: 'GENERATE_PDF', defaultValue: true, description: '是否生成PDF报告')
        string(name: 'PARMMS_1', description: '所需要的其他参数')
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
                        // 配置Git使用更安全的TLS设置
                        sh 'git config --global http.sslVerify false'
                        sh 'git config --global http.version HTTP/1.1'
                        checkout scm

                        // 运行测试和构建
                        runTestSuite('main')
                    }
            }
            post {
                always {
                        generateReports()
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
                        // 配置Git使用更安全的TLS设置
                        sh 'git config --global http.sslVerify false'
                        sh 'git config --global http.version HTTP/1.1'
                        checkout([$class: 'GitSCM', branches: [[name: "*/main"]], userRemoteConfigs: [[url: "${REPO_URL}"]]])

                        // 构建镜像
                        buildAndPushImage("hello-world-service")

                        // 运行冒烟测试
                        runTestSuite('SMOKE')
                    }
            }
            post {
                always {
                        generateReports()
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
                        // 配置Git使用更安全的TLS设置
                        sh 'git config --global http.sslVerify false'
                        sh 'git config --global http.version HTTP/1.1'
                        checkout([$class: 'GitSCM', branches: [[name: "*/main"]], userRemoteConfigs: [[url: "${REPO_URL}"]]])

                        // 构建镜像
                        buildAndPushImage("hello-world-service")

                        // 运行全量测试
                        runTestSuite('FULL')
                    }
            }
            post {
                always {
                        generateReports()
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

        // ============================ 报告汇总 ============================
        stage('Collect Reports') {
            steps {
                script {
                        echo "Collecting all logs and reports..."
                        sh "mkdir -p ${REPORT_DIR} ${ALLURE_DIR}"

                        // 归档测试报告
                        archiveArtifacts artifacts: 'tests/reports/**', allowEmptyArchive: true
                        archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true

                        // 生成Allure报告
                        generateAllureReport()

                        // 生成PDF报告
                        if (params.GENERATE_PDF) {
                            generatePDFReport()
                        }
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

// 构建并推送镜像
def buildAndPushImage(imageName) {
        def fullImageName = "${env.DOCKER_REGISTRY}/${imageName}"
        def dateTag = "daily-${new Date().format('yyyyMMdd')}"
        def gitCommit = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()

        echo "Building Docker image: ${fullImageName}"

        // 构建wheel包
        sh "python setup.py bdist_wheel"
        stash includes: 'dist/*.whl', name: 'wheel'

        // 构建Docker镜像
        sh """
        docker build -f Dockerfile -t ${fullImageName}:${dateTag} .
        docker tag ${fullImageName}:${dateTag} ${fullImageName}:${gitCommit}
        docker tag ${fullImageName}:${dateTag} ${fullImageName}:latest

        # 如果配置了Docker Hub凭据，则推送镜像
        if [ ! -z "${DOCKER_HUB_USER}" ] && [ ! -z "${DOCKER_HUB_TOKEN}" ]; then
            echo ${DOCKER_HUB_TOKEN} | docker login -u ${DOCKER_HUB_USER} --password-stdin
            docker push ${fullImageName}:${dateTag}
            docker push ${fullImageName}:${gitCommit}
            docker push ${fullImageName}:latest
            docker logout
        else
            echo "Docker Hub credentials not configured, skipping image push"
        fi
        """
}

// 运行测试套件
def runTestSuite(testType) {
        echo "===== Running ${testType} Test Suite ====="

        try {
            // 启动测试环境
            sh "docker-compose -f docker-compose.test.yml up -d --build"

            // 等待服务就绪
            sh """
            # 等待服务启动
            timeout 300 bash -c 'until curl -f http://localhost:5000/health; do sleep 5; done'
            """

            // 运行测试
            sh "docker-compose -f docker-compose.test.yml run --rm test pytest -v --tb=short --alluredir=allure-results"

        } catch (Exception e) {
            echo "Test execution failed: ${e.getMessage()}"
            currentBuild.result = 'FAILURE'
            throw e
        }
}

// 生成报告
def generateReports() {
        echo "Generating test reports..."

        // 收集测试结果
        sh "mkdir -p ${REPORT_DIR} ${ALLURE_DIR}"

        // 复制测试报告
        sh "cp -r tests/reports/* ${REPORT_DIR}/ || true"
        sh "cp -r allure-results/* ${ALLURE_DIR}/ || true"
}

// 生成Allure报告
def generateAllureReport() {
    echo "Generating Allure report..."
    
    // 使用Allure Jenkins插件生成报告
    allure([
        includeProperties: false,
        jdk: '',
        properties: [],
        reportBuildPolicy: 'ALWAYS',
        results: [[path: "${ALLURE_DIR}"]]
    ])
}

// 生成PDF报告
def generatePDFReport() {
        echo "Generating PDF report..."

        sh """
        # 使用预安装的Python和脚本生成PDF报告
        if [ -f "scripts/generate_pdf_report.py" ]; then
            python scripts/generate_pdf_report.py
        else
            echo "PDF generation script not found, skipping"
        fi
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
                <p><strong>Allure Report:</strong> <a href="${env.BUILD_URL}allure">${env.BUILD_URL}allure</a></p>

                <h3>Test Summary</h3>
                <p>Please check the attached reports for detailed test results.</p>

                <p>Best regards,<br>Jenkins CI/CD System</p>
            </body>
            </html>
            """

            try {
                // 发送邮件
                emailext(
                    subject: subject,
                    body: body,
                    to: "${EMAIL_RECIPIENTS}",
                    attachmentsPattern: 'tests/reports/*.pdf',
                    mimeType: 'text/html'
                )
            } catch (Exception e) {
                echo "Failed to send email notification: ${e.getMessage()}"
                // 邮件发送失败不应该影响构建结果
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