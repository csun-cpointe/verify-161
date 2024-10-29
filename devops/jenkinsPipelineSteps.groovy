/*-
 * #%L
 * AIOps Foundation::Archetype::Project
 * %%
 * Copyright (C) 2021 Booz Allen
 * %%
 * All Rights Reserved. You may not copy, reproduce, distribute, publish, display, 
 * execute, modify, create derivative works of, transmit, sell or offer for resale, 
 * or in any way exploit any part of this solution without Booz Allen Hamilton’s 
 * express written permission.
 * #L%
 */
/**
 * Common steps for pipelines
 */
def argocdAuthenticate(argocdUrl, argocdPassword) {
    sh '''
        # Check if Argocd is installed
        if ! type "/usr/local/bin/argocd" > /dev/null; then
            echo "Installing Argocd..."
            sudo curl --silent --location -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
            sudo chmod +x /usr/local/bin/argocd
            /usr/local/bin/argocd version --client
        fi
    '''
    sh "/usr/local/bin/argocd login ${argocdUrl} --username admin --password ${argocdPassword} --skip-test-tls --grpc-web"

}

def argocdTerminate(argocdAppName) {
    try {
       sh "/usr/local/bin/argocd app delete ${argocdAppName} --grpc-web"
    } catch (err) {
        slackSend color: "warning",
                    message: "Verify 161 app not found on the server, deploying..."
        echo "App name not found on the server, deploying..."
    }
}

def argocdSync(argocdAppName, argocdBranch) {
    String argocdSyncLabel = "argocd.argoproj.io/instance=${argocdAppName}"
    sh "sleep 10"
    sh "/usr/local/bin/argocd app sync ${argocdAppName} --grpc-web --revision ${argocdBranch}"
    sh "sleep 10"
    sh "/usr/local/bin/argocd app sync -l ${argocdSyncLabel} --grpc-web --revision ${argocdBranch}"
}

def argocdDeploy(argocdAppName, argocdUrl, argocdDestinationServer, gitRepo, argocdBranch, argocdNamespace, values) {
    String valuesParam = "--values " + values.join(" --values ")
    sh "sleep 60" //wait for app to shutdown before creation
    sh "/usr/local/bin/argocd app create ${argocdAppName} --grpc-web \
            --server ${argocdUrl} \
            --dest-namespace ${argocdNamespace} \
            --dest-server ${argocdDestinationServer} \
            --repo ${gitRepo} \
            --path verify-161-deploy/src/main/resources --revision ${argocdBranch} \
            ${valuesParam}"
    try {
        argocdSync(argocdAppName, argocdBranch)
    } catch (err) {
        echo "Sync failed, retrying..."
        slackSend color: "warning",
                    message: "Verify 161 Argocd sync failed, retrying..."
        retry(3) {
            argocdSync(argocdAppName, argocdBranch)
        }
    }
}

return this
