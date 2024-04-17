pipeline {
    agent any
    options {
        skipStagesAfterUnstable()
    }
    stages {
         stage('Clone repository') { 
            steps { 
                script{
                checkout scm
                }
            }
        }

        stage('Build') { 
            steps { 
                script{
                 app = docker.build("students")
                }
            }
        }
        stage('Test'){
            steps {
                 echo 'Empty'
            }
        }
        stage('configure docker') {
            steps {
                 sh '''#!/bin/bash
                         mv $HOME/.docker/config.json $HOME/.docker/config.json.backup
                         kubectl version
                 '''
            }
        }
        stage('Deploy') {
            steps {
                script{
                        docker.withRegistry('https://765449138108.dkr.ecr.us-east-1.amazonaws.com/students', 'ecr:us-east-1:Admin') {
                    app.push("${env.BUILD_NUMBER}")
                    app.push("latest")
                    }
                }
            }
        }
    }
}
