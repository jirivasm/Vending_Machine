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
                    script {
                        // Use the credential ID you created in Jenkins
                        docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-creds') {
                            def myImage = docker.build("jirivasm/vending-app:1.0.${env.BUILD_ID}", "./VendingMachineApp")
                            myImage.push()
                            myImage.push("latest")
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            container('docker') {
                sh "docker rmi -f jirivasm/vending-app:1.0.${env.BUILD_ID} || true"
                sh "docker rmi -f jirivasm/vending-app:latest || true"
            }
        }
    }
}