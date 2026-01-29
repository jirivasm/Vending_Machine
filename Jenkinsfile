pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: jirivasm/custom-jenkins:latest
    command: ['cat']
    tty: true
    securityContext:
      runAsUser: 0      
    volumeMounts:
    - mountPath: /var/run/docker.sock
      name: docker-sock
  volumes:
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
"""
        }
    }
    
    stages {
        stage('Check Environment') {
            steps {
                container('docker') {
                    sh 'docker --version'
                }
            }
        }       
        
        stage('Prepare') {
            steps {
                echo 'Checking out the repo...'
                checkout scm
            }
        }

        stage('Build and Test') {
            steps {
                container('docker') {
                    // Using your confirmed VendingMachineApp directory
                    sh 'docker build -t vending-app ./VendingMachineApp'
                    sh 'docker run --rm vending-app python -m unittest test_vending_machine'
                }
            }
        } 

        stage('Push To Registry') {
            steps {
                container('docker') {
                    // Use standard shell commands instead of the 'docker' groovy object
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'DOCKER_HUB_PASSWORD', usernameVariable: 'DOCKER_HUB_USER')]) {
                        sh "echo \$DOCKER_HUB_PASSWORD | docker login -u \$DOCKER_HUB_USER --password-stdin"
                        sh "docker build -t jirivasm/vending-app:1.0.${env.BUILD_ID} ./VendingMachineApp"
                        sh "docker tag jirivasm/vending-app:1.0.${env.BUILD_ID} jirivasm/vending-app:latest"
                        sh "docker push jirivasm/vending-app:1.0.${env.BUILD_ID}"
                        sh "docker push jirivasm/vending-app:latest"
                    }
                }
        }
    }

    post {
        always {
            container('docker') {
                sh "docker rmi -f jirivasm/vending-app:${env.BUILD_ID} || true"
                sh "docker rmi -f jirivasm/vending-app:latest || true"
            }
        }
    }
}