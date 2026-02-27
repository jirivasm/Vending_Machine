pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  # Run the build on the Raspberry Pi nodes
  nodeSelector:
    kubernetes.io/arch: arm64
  containers:
  - name: jnlp
    image: jenkins/inbound-agent:latest
    resources:
      requests:
        memory: "512Mi"
        cpu: "500m"
      limits:
        memory: "2Gi"
        cpu: "1000m"
        
  # NEW: A native Python container just for running your unit tests
  - name: python-tester
    image: python:3.11-slim
    command: ['sleep', '99d']
    
  # The Kaniko builder
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug
    command: ['sleep', '99d']
    volumeMounts:
    - name: kaniko-secret
      mountPath: /kaniko/.docker
      
  volumes:
  - name: kaniko-secret
    secret:
      secretName: regcred
      items:
      - key: .dockerconfigjson
        path: config.json
"""
        }
    }
    
    stages {
        stage('Prepare') {
            steps {
                echo 'Checking out the repo...'
                checkout scm
            }
        }

        stage('Run Unit Tests') {
            steps {
                // Run the tests natively inside the Python container
                container('python-tester') {
                    dir('VendingMachineApp') {
                        sh '''
                        echo "--- Running Unit Tests (In-Memory DB) ---"
                        pip install --no-cache-dir -r requirements.txt
                        export TESTING=true
                        
                        python -m unittest test_vending_machine
                        '''
                    }
                }
            }
        } 

        stage('Build and Push') {
            steps {
                container('kaniko') {
                    // Note: Context and Dockerfile paths updated for the VendingMachineApp subfolder
                    sh """
                    /kaniko/executor \
                      --context ${WORKSPACE}/VendingMachineApp \
                      --dockerfile ${WORKSPACE}/VendingMachineApp/dockerfile \
                      --destination jirivasm/vending-app:3.0.${env.BUILD_ID} \
                      --destination jirivasm/vending-app:latest
                    """
                }
            }
        }
    }
}