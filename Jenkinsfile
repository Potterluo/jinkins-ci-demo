pipeline{
    environment{
        DOCKER_REGISTRY = '127.0.0.1:5000'
        REPORT_DIR      = 'report_pdf'
        // 邮件接收人
        MAIL_LIST       = 'your-team@example.com'
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
