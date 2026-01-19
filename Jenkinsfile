pipeline{
    agent any
    
    stages{
        stage ('Prepare'){
            steps {
                echo 'checking out the repo...'
                checkout scm
                echo 'Code Checked out Succesfully'
            }
        }
        stage('Build and Test') {
        steps {
            script {
                sh 'docker build -t jirivasm/vending-app:test ./VendingMachineApp'
                sh 'docker run jirivasm/vending-app:test python3 -m unittest testVendingMachine.py'
            }
        }
    }   
        stage ('Push To registry'){
            steps {
                echo 'Deploying to Dockerhub'
                // This step should not normally be used in your script. Consult the inline help for details.
                script{
                    docker.withRegistry('https://index.docker.io/v1/', 'Docker_Hub' ) {
                    // some block
                    def myImage = docker.build("jirivasm/vending-app:${env.BUILD_ID}","./VendingMachineApp")
                    myImage.push()
                    myImage.push("latest")
                    }
                }
            }
        }
    }
    post {
        always {
            echo 'Cleaning up local Docker images...'
            script {
                // This removes the specific image built in this run
                // The '|| true' ensures the pipeline doesn't fail if the image was already gone
                sh "docker rmi jirivasm/vending-app:${env.BUILD_ID} || true"
                sh "docker rmi jirivasm/vending-app:latest || true"
            }
        }
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Pipeline failed. Check the logs for errors.'
        }
    }
}