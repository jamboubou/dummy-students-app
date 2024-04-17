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
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh '''#!/bin/bash
                            aws eks update-kubeconfig --region us-east-1 --name EKSClusterE11008B6-ef81e24701dc4f909b213b97c275033c
                            kubectl get pods
                            mv $HOME/.docker/config.json $HOME/.docker/config.json.backup
                    '''
                }
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
