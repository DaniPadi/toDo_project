// Jenkinsfile (mínimo para validar clon + polling)
pipeline {
  agent any
  options { timestamps(); disableConcurrentBuilds() }
  triggers { pollSCM('H/2 * * * *') } // revisa cambios aprox. cada 2 min
  stages {
    stage('Checkout') {
      steps {
        // Reemplaza USER y REPO
        git url: 'https://github.com/DaniPadi/toDo_project.git',
            branch: 'master',
            credentialsId: 'github-https'  // o 'github-ssh' si usas SSH
      }
    }
    stage('Sanity') {
      steps {
        sh 'ls -la'
      }
    }
  }
}
