pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build('my-flask-app:latest', '-f Dockerfile.flask .')
                }
            }
        }
    }

    stages {
        stage('Prepare Scripts') {
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
                        sh '''
                            pip install selenium webdriver-manager pytest
                            apt-get update && apt-get install -y wget unzip
                            wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
                            apt install -y ./google-chrome-stable_current_amd64.deb
                            wget https://chromedriver.storage.googleapis.com/$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
                            unzip chromedriver_linux64.zip
                            mv chromedriver /usr/local/bin/
                        '''
                        sh 'mkdir -p logs'
                        script {
                            try {
                                sh 'pytest test_app.py --junitxml=logs/integration_test_results.xml'
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
            junit testResults: 'logs/**/*.xml', allowEmptyResults: true
        }
    }
}