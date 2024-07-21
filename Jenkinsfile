pipeline {
    agent none
    stages {
        stage('Prepare Scripts') {
            agent any
            steps {
                sh 'git update-index --chmod=+x jenkins/scripts/deploy.sh'
                sh 'git update-index --chmod=+x jenkins/scripts/kill_integration.sh'
            }
        }
        stage('Install Dependencies') {
            agent {
                docker {
                    image 'python:latest'
                    args '-u root'
                }
            }
            steps {
                sh 'pip install pytest pytest-cov selenium webdriver-manager'
            }
        }
        stage('Run Unit Tests') {
            agent {
                docker {
                    image 'python:latest'
                    args '-u root'
                }
            }
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
            post {
                always {
                    junit testResults: 'logs/unitreport.xml', allowEmptyResults: true
                }
            }
        }
        stage('Integration UI Test') {
            parallel {
                stage('Deploy') {
                    agent any
                    steps {
                        sh './jenkins/scripts/deploy.sh'
                        input message: 'Finished using the web site? (Click "Proceed" to continue)'
                        sh './jenkins/scripts/kill_integration.sh'
                    }
                }
                stage('Headless Browser Test') {
                    agent {
                        docker {
                            image 'python:latest'
                            args '-u root'
                        }
                    }
                    steps {
                        sh 'pip install selenium webdriver-manager'
                        sh 'mkdir -p logs'
                        script {
                            try {
                                sh 'python test_app.py --junitxml=logs/integration_test_results.xml'
                            } catch (Exception e) {
                                echo "Integration tests failed: ${e.message}"
                                currentBuild.result = 'FAILURE'
                            }
                        }
                    }
                    post {
                        always {
                            junit 'logs/integration_test_results.xml'
                        }
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
