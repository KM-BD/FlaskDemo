pipeline {
    agent {
        docker {
            image 'python:latest' // Using the latest Python Docker image
            args '-u root' // Run as root to avoid permission issues
        }
    }
    environment {
        PYTHONUSERBASE = "${env.WORKSPACE}/.local" // Set a user base for pip installations
        PATH = "${env.WORKSPACE}/.local/bin:${env.PATH}" // Add the local bin to PATH
    }
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install --user pytest pytest-cov' // Install dependencies in user-specific directory
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pytest --junitxml=logs/unitreport.xml tests/' // Run pytest and generate a JUnit XML report
            }
        }
    }
    post {
        always {
            junit testResults: 'logs/unitreport.xml' // Archive the test results
        }
    }
}
