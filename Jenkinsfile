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
                    sh 'ls -l /var/run/docker.sock'
        
                    // 2. Check who the container thinks it is
                    sh 'id'
                    
                    // 3. Try the command again
                    sh 'docker ps'
                }
            }
        }       
        
        stage('Prepare') {
            steps {
                echo 'Checking out the repo...'
                checkout scm
                container('docker') {
                    echo 'Register QEMU handlers ONCE'
                    sh 'docker run --privileged --rm tonistiigi/binfmt --install all'
                }
            }
        }

        stage('Build and Test') {
            steps {
                container('docker') {

                    script{
                        // Register QEMU handlers in the host kernel via the container
                        
                        sh 'docker buildx create --use --name mybuilder || true'
                        // Using your confirmed VendingMachineApp directory
                        sh 'docker buildx build --platform linux/amd64 -t vending-app --load ./VendingMachineApp'
                        echo '--- Running Unit Tests (In-Memory DB) ---'
                        sh 'docker run --rm -e TESTING=true vending-app python -m unittest test_vending_machine'
                    }
                }
            }
        } 

        stage('Push To Registry') {
            steps {
                container('docker') {
                    
                    // Use standard shell commands instead of the 'docker' groovy object
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'DOCKER_HUB_PASSWORD', usernameVariable: 'DOCKER_HUB_USER')]) {
                        sh 'docker buildx create --use --name mybuilder || true'
                        sh "echo \$DOCKER_HUB_PASSWORD | docker login -u \$DOCKER_HUB_USER --password-stdin"
                        sh """
                        docker buildx build --platform linux/amd64,linux/arm64 \
                        -t jirivasm/vending-app:2.0.${env.BUILD_ID}  \
                        -t jirivasm/vending-app:latest \
                        --push ./VendingMachineApp
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            container('docker') {
                sh "docker rmi -f vending-app || true"
                sh "docker rmi -f jirivasm/vending-app:2.0.${env.BUILD_ID} || true"
                sh "docker rmi -f jirivasm/vending-app:latest || true"
                sh 'docker buildx rm mybuilder || true'
            }
        }
    }
}