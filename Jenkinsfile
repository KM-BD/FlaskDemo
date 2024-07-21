pipeline {
    agent {
        docker {
            image 'python:latest'
            args '-u root'
        }
    }
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install pytest pytest-cov'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'mkdir -p logs'
                script {
                    try {
                        sh 'pytest --junitxml=logs/unitreport.xml tests/'
                    } catch (Exception e) {
                        echo "pytest failed: ${e.message}"
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }
    }
    post {
        always {
            junit testResults: 'logs/unitreport.xml', allowEmptyResults: true
        }
    }
}