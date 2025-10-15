pipeline{
    agent { label 'master' }          // 如要无固定 agent，可改回 agent none
    environment{
        DOCKER_REGISTRY = '127.0.0.1:5000'
        REPORT_DIR      = 'report_pdf'
        // 邮件接收人
        MAIL_LIST       = 'your-team@example.com'
    }
    parameters{
        string(name: 'MANUAL_BRANCH', defaultValue: 'main', description: '手动构建分支')
        choice(name: 'TRIGGER_TYPE', choices: ['PR_VERIFY', 'DAILY_BUILD'], description: '触发类型')
    }
    triggers{
        cron('H 0 * * *')             // 每日凌晨
    }
    options{
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    stages{
        // ================ PR 验证 / 手动 PR_VERIFY ===================
        stage('PR Verification'){
            when {
                anyOf{
                    branch 'PR-*'
                    expression { params.TRIGGER_TYPE == 'PR_VERIFY' }
                }
            }
            steps{
                script{
                    echo "===== Starting PR Verification ====="
                    checkout scm
                    // 服务镜像
                    sh "bash scripts/build.sh app/app app/Dockerfile"
                    // 测试镜像
                    sh "docker build -t vllm-uc-test:latest -f tests/Dockerfile tests/"
                    // 启动 compose（app+test 同一网络）
                    sh """
                    docker network create uc-net || true
                    docker run -d --rm --name app --network uc-net \
                           ${DOCKER_REGISTRY}/app:daily-$(date +%Y%m%d)
                    docker run --rm --name test --network uc-net \
                           -v \$(pwd)/allure-results:/tests/allure-results \
                           -v \$(pwd)/report_pdf:/tests/report_pdf \
                           vllm-uc-test:latest
                    docker stop app
                    docker network rm uc-net || true
                    """
                }
            }
        }
        // ================ 日构建 & 冒烟 ===================
        stage('Daily Build & Smoke Test'){
            when {
                anyOf{
                    triggeredBy 'TimerTrigger'
                    expression { params.TRIGGER_TYPE == 'DAILY_BUILD' }
                }
            }
            steps{
                script{
                    checkout([$class: 'GitSCM',
                              branches: [[name: "*/${params.MANUAL_BRANCH}"]],
                              userRemoteConfigs: scm.userRemoteConfigs])
                    // 复用上面脚本
                    sh "bash scripts/build.sh app/app app/Dockerfile"
                    sh "docker build -t vllm-uc-test:latest -f tests/Dockerfile tests/"
                    sh """
                    docker network create uc-net || true
                    docker run -d --rm --name app --network uc-net \
                           ${DOCKER_REGISTRY}/app:daily-$(date +%Y%m%d)
                    docker run --rm --name test --network uc-net \
                           -v \$(pwd)/allure-results:/tests/allure-results \
                           -v \$(pwd)/report_pdf:/tests/report_pdf \
                           vllm-uc-test:latest
                    docker stop app
                    docker network rm uc-net || true
                    """
                }
            }
        }
        // ================ 生成 Allure + PDF ===================
        stage('Collect Reports'){
            steps{
                sh "pip install allure-combine weasyprint -i https://pypi.tuna.tsinghua.edu.cn/simple"
                sh "python scripts/pdf_report.py"
            }
        }
    }
    post{
        always{
            // 1. 发布 Allure HTML
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'allure-results']]
            ])
            // 2. 归档
            archiveArtifacts artifacts: 'report_pdf/*.pdf', allowEmptyArchive: false
            // 3. 邮件
            emailext(
                subject: "【${currentBuild.currentResult}】${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                <p>构建结果：<b>${currentBuild.currentResult}</b></p>
                <p>Allure 报告：<a href="${BUILD_URL}allure">${BUILD_URL}allure</a></p>
                <p>详见附件 PDF。</p>
                """,
                to: "${env.MAIL_LIST}",
                attachmentsPattern: 'report_pdf/*.pdf',
                mimeType: 'text/html'
            )
            echo "Pipeline Finished: ${currentBuild.currentResult}"
        }
    }
}