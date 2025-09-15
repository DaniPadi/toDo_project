pipeline {
  agent any
  options { timestamps(); disableConcurrentBuilds() }
  triggers { pollSCM('H/2 * * * *') } // quítalo si ya activaste Poll SCM en el job
  environment {
    // Evita prompt si no tienes known_hosts listo; opcional:
    GIT_SSH_COMMAND = 'ssh -o StrictHostKeyChecking=accept-new'
  }
  stages {
    stage('Checkout') {
      steps {
        git url: 'git@github.com:DaniPadi/toDo_project.git',
            branch: 'master',
            credentialsId: 'github-ssh'
      }
    }
    stage('Sanity') {
      steps {
        sh 'docker-compose up -d'
      }
    }
  }
}
