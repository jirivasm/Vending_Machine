pipeline{
    agent any
    
    stages{
        stage ('Prepare'){
            steps {
                echo 'checking out the repo...'
                checkout scm
                echo 'Code Checked out Succesfully'
                sh 'cd'
                sh ' pip install -r requirements.txt'
                
            }
        }
        stage ('Build and Test')
            steps {
                echo 'Testing the app'
                sh 'python test_vending_machine.py'
            }
        stage ('Push To registry'){
            steps {
                echo 'Deploying to Dockerhub'
                // This step should not normally be used in your script. Consult the inline help for details.
                withDockerRegistry(credentialsId: 'Docker_Hub') {
                // some block
                def myImage = docker.build("jirivasm/vending-app:${env.BUILD_ID}","./VendingMachineApp")
                myImage.Push()
                myImage.Push("latest")
                }
            }
        }
    }
}