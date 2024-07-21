pipeline {
    agent any
    stages {
        stage('Checkout SCM') {
            steps {
                // Checkout the code from the repository
                git branch: 'main', url: 'https://github.com/Thrith10/FlaskDemo.git'
            }
        }
        stage('Build') {
            steps {
                script {
                    docker.image('node:14').inside {
                        sh 'npm install'
                    }
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    docker.image('node:14').inside {
                        sh 'chmod +x jenkins/scripts/test.sh'
                        sh 'jenkins/scripts/test.sh'
                    }
                }
            }
        }
        stage('OWASP Dependency-Check Vulnerabilities') {
            steps {
                dependencyCheck additionalArguments: ''' 
                            -o './'
                            -s './'
                            -f 'ALL' 
                            --prettyPrint''', odcInstallation: 'OWASP Dependency-Check Vulnerabilities'
        
                dependencyCheckPublisher pattern: 'dependency-check-report.xml'
            }
        }
    }
    post {
        always {
            junit 'logs/unitreport.xml'
        }
    }
}
