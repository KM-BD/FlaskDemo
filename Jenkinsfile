pipeline {
    agent {
        docker {
            image 'python:latest' // Using the latest Python Docker image
        }
    }
    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt' // Install dependencies from requirements.txt
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
