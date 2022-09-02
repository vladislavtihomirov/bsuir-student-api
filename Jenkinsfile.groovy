def branch_name = "master"

timestamps{
  try {
        notifyBuildStatus('STARTED')
        if(k8sEnv == "prod"){
            CR_FILE = "prod-logging-k8s-rancher-admin.config"
            HOSTNAME = "api-mi.backend-capital.com"
        }
        else {
            CR_FILE = "test-rancher-aws2.config"
            HOSTNAME = "test-api-mi.backend-capital.com"
        }

        if (branch != '') {
            branch_name = branch.replace("origin/", "")
        }

        echo "branch ${branch_name}"

        node {
            stage("Building marketing intelligence api container") {
                git credentialsId: 'jenkins-ci-ssh', url: 'ssh://git@gitlab.itcapital.io:8022/mi/mi-communications/segmentation/mi-api-py.git', branch:  "${branch_name}"

                String deployment_file = readFile "cd/deployment/mi-api-py-${k8sEnv}.yml"
                deployment_file = deployment_file.replaceAll("ENV", "${k8sEnv}")
                deployment_file = deployment_file.replaceAll("HOSTNAME", "${HOSTNAME}")
                writeFile(file: "cd/mi-api-py-deployment.yml", text: deployment_file)


                def docker_img = docker.build "171350417925.dkr.ecr.eu-west-1.amazonaws.com/marketing-intelligence", "-f Dockerfile ."

                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'jenkins-ci_capital.com']]) {
                    sh '$(aws ecr get-login --region eu-west-1 --no-include-email)'
                    docker_img.push "mi-api-py-${k8sEnv}-${BUILD_ID}"
                    docker_img.push "mi-api-py-${k8sEnv}-latest"
                }
            }

            stage("Make mi-api-py up and running") {
                withCredentials([file(credentialsId: "${CR_FILE}", variable: 'FILE')]) {
                    sh "kubectl-1.12.3 apply -f cd/mi-api-py-deployment.yml --kubeconfig \"${FILE}\""
                    def podState = sh(returnStdout: true, script: "kubectl-1.12.3 -n mi --kubeconfig \"${FILE}\" get pods | grep -E \"mi.+Running\" || true").trim()

                    print podState

                    if (podState.size() > 2) {
                        // looks like it's not a new pod so let's try to update image for it
                        sh "kubectl-1.12.3 -n mi --kubeconfig \"${FILE}\" set image deployment/mi-api-py-deployment mi-api-py=171350417925.dkr.ecr.eu-west-1.amazonaws.com/marketing-intelligence:mi-api-py-${k8sEnv}-${BUILD_ID}"
                    }
                }
            }
        }
    } catch (e) {
      currentBuild.result = "FAILED"
      throw e
    } finally {
    notifyBuildStatus (currentBuild.result)
  }
}

def notifyBuildStatus ( String buildStatus = 'STARTED') {
    buildStatus = (buildStatus ?: 'SUCCESS')
    if (buildStatus == 'STARTED') {
        color = 'good'
        message = "ENV:${k8sEnv} ${buildStatus}: Job ${env.JOB_NAME} #${env.BUILD_NUMBER}."
    } else if (buildStatus == 'SUCCESS') {
        color = 'good'
        message = "ENV:${k8sEnv} ${buildStatus}: Job ${env.JOB_NAME} #${env.BUILD_NUMBER}."
    } else {
        color = '#FF0000'
        message = "ENV:${k8sEnv} ${buildStatus}: Job ${env.JOB_NAME} #${env.BUILD_NUMBER}.\n${BUILD_URL}"
    }

    slackSend ( channel: "U014L5L12M8", color: color, message: message) // Alexander Sokolovskiy
    slackSend ( channel: "U2Q5HSM1Q", color: color, message: message) // Pavel Prylutski

//     slackSend ( channel: '#mi-alert', color: color, message: message)
}
