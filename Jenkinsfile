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
        stage('================ PR 验证 / 手动 PR_VERIFY ==================='){
            steps{
                script{
                    echo "===== Starting PR Verification ====="
                }
            }
        }
        // ================ 生成 Allure + PDF ===================
        stage('Collect Reports'){
            steps{
                script{
                    echo "================ 生成 Allure + PDF ==================="
                }
            }
        }
    }
    post{ 
        success {
            echo '✅ Deployment succeeded!'
        }
        failure {
            echo '❌ Deployment failed!'
        }
        always {
            // 清理或通知
            echo 'Cleanup or notification here.'
        }
    }
}
