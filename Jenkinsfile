pipeline {
    agent any
    stages {
        stage('Checkout SCM') {
            steps {
                // Checkout the code from the repository
                git branch: 'main', url: 'https://github.com/Thrith10/FlaskDemo.git'
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
}
