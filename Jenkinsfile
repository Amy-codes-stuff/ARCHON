
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
                echo 'Checking Python version...'
                bat '"C:\\Users\\tiwar\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" --version'

                echo 'Checking Python syntax...'
                bat '"C:\\Users\\tiwar\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" -m compileall -q communication coordinator dashboard nodes'

                echo 'Python syntax check completed successfully.'
            }
        }

        stage('Test') {
            steps {
                echo 'Running ARCHON middleware smoke test...'
                bat '"C:\\Users\\tiwar\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" nodes\\middleware_test.py'
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
