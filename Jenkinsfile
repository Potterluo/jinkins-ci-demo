pipeline{
    agent none  // 不使用任何固定 agent，仅在主节点调度
    environment{
        DOCKER_REGISTRY = '127.0.0.1:5000'
        REPORT_DIR      = 'report_pdf'
        // 邮件接收人
        MAIL_LIST       = 'your-team@example.com'
    }
    parameters{
        string(name: 'MANUAL_BRANCH', defaultValue: 'main', description: '手动构建分支')
        choice(name: 'TRIGGER_TYPE', choices: ['PR_VERIFY', 'DAILY_BUILD', 'FULL_TEST'], description: '触发类型')
        string(name: 'Params1', defaultValue: 'xxx', description: '测试所学参数')
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
            when {
                anyOf {
                    branch 'PR-*'
                    expression { params.TRIGGER_TYPE == 'PR_VERIFY' }
                }
            }
            steps{
                script{
                    echo "===== Starting PR Verification ====="
                }
            }
        }
        // ================ 日构建 ===================
        stage('Daily Build & Smoke Test'){
            when {
                anyOf {
                    triggeredBy 'TimerTrigger'
                    expression { params.TRIGGER_TYPE == 'DAILY_BUILD' }
                }
            }
            steps{
                script{
                    echo "================ 日构建 ==================="
                }
            }
        }

        // ================ 全量构建 ===================
        stage('Full Test'){
             when { expression { params.TRIGGER_TYPE == 'FULL_TEST' } }
            steps{
                script{
                    echo "================ 全量构建 ==================="
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
