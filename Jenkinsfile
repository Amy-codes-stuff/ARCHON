pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out ARCHON source code from GitHub'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Checking Python syntax...'
                bat 'python --version'
                bat 'python -m compileall -q communication coordinator dashboard nodes'
                echo 'Python syntax check completed.'
            }
        }

        stage('Test') {
            steps {
                echo 'Running ARCHON middleware smoke test...'
                bat 'python nodes\\middleware_test.py'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deployment stage reached.'
                echo 'No live deployment is performed in this assignment.'
            }
        }
    }

    post {
        success {
            echo 'ARCHON CI/CD pipeline completed successfully!'
        }
        failure {
            echo 'ARCHON CI/CD pipeline failed. Check the stage logs.'
        }
    }
}
