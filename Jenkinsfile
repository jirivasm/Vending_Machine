pipeline{
    agent {
        kubernetes {
            yaml """
            apiVersion: v1
            kind: Pod
            spec:
            containers:
            - name: docker
                image: jirivasm/custom-jenkins:latest  # Using your custom image
                command: ['cat']
                tty: true
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
    
    stages{
        stage('Check Environment') {
            steps {
            sh 'docker --version'
            }
        }       
    //     stage ('Prepare'){
    //         steps {
    //             echo 'checking out the repo...'
    //             checkout scm
    //             echo 'Code Checked out Succesfully'
    //         }
    //     }
    //     stage('Build and Test') {
    //         steps {
           
    //         // Build using the Dockerfile you just shared
    //         sh 'docker build -t vending-app ./VendingMachineApp'
        
    //         // Run the test - notice there is NO .py extension
    //         sh 'docker run --rm vending-app python -m unittest test_vending_machine'
    //         }
    //     } 
    //     stage ('Push To registry'){
    //         steps {
    //             echo 'Deploying to Dockerhub'
    //             // This step should not normally be used in your script. Consult the inline help for details.
    //             script{
    //                 docker.withRegistry('https://index.docker.io/v1/', 'docker-credentials' ) {
    //                 // some block
    //                 def myImage = docker.build("jirivasm/vending-app:1.0.${env.BUILD_ID}","./VendingMachineApp")
    //                 myImage.push()
    //                 myImage.push("latest")
    //                 }
    //             }
    //         }
    //     }
    }
    // post {
    //     always {
    //         echo 'Cleaning up local Docker images...'
    //         script {
    //             // This removes the specific image built in this run
    //             // The '|| true' ensures the pipeline doesn't fail if the image was already gone
    //             sh "docker rmi jirivasm/vending-app:${env.BUILD_ID} || true"
    //             sh "docker rmi jirivasm/vending-app:latest || true"
    //         }
    //     }
    //     success {
    //         echo 'Deployment successful!'
    //     }
    //     failure {
    //         echo 'Pipeline failed. Check the logs for errors.'
    //     }
    // }
}