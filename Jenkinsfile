pipeline{
    agent any
    
    stages{
        stage('Check Environment') {
            steps {
            sh 'docker --version'
            }
        }       
        stage ('Prepare'){
            steps {
                echo 'checking out the repo...'
                checkout scm
                echo 'Code Checked out Succesfully'
            }
        }
        stage('Build and Test') {
        steps {
            script{
                // 1. Build the image once and store it in a variable
                def testImage = docker.build("vending-app-test", "./VendingMachineApp")
                // 2. Run tests inside a temporary container from that image
                // This 'inside' block automatically handles the --rm cleanup
                testImage.inside {
                sh 'python -m unittest test_vending_machine'
                }   
            }
                
            }
        } 
        stage ('Push To registry'){
            steps {
                echo 'Deploying to Dockerhub'
                // This step should not normally be used in your script. Consult the inline help for details.
                script{
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-credentials' ) {
                    // some block
                    def myImage = docker.build("jirivasm/vending-app:1.0.${env.BUILD_ID}","./VendingMachineApp")
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