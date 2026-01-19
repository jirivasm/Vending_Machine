pipeline{
    agent any
    
    stages{
        stage ('Prepare'){
            steps {
                echo 'checking out the repo...'
                checkout scm
                echo 'Code Checked out Succesfully'
                sh 'cd && pip install -r requirements.txt'
            }
        }
        stage ('Build and Test') {
            steps {
                echo 'Testing the app'
                sh 'python test_vending_machine.py'
            }
        }
        stage ('Push To registry'){
            steps {
                echo 'Deploying to Dockerhub'
                // This step should not normally be used in your script. Consult the inline help for details.
                Docker.withRegistry('https://index.docker.io/v1/', 'Docker_Hub' ) {
                // some block
                def myImage = docker.build("jirivasm/vending-app:${env.BUILD_ID}","./VendingMachineApp")
                myImage.push()
                myImage.push("latest")
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