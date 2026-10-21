
pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        PYTHON = 'C:\\Users\\tiwar\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe'
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out ARCHON from GitHub'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Checking Python version...'
                bat '"%PYTHON%" --version'

                echo 'Checking Python syntax...'
                bat '"%PYTHON%" -m compileall -q communication coordinator dashboard nodes'

                echo 'Python syntax check passed.'
            }
        }

        stage('Test') {
            steps {
                echo 'Running ARCHON middleware smoke test...'
                bat '"%PYTHON%" nodes\\middleware_test.py'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deployment stage reached.'
                echo 'No live deployment is performed.'
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
