pipeline {
    agent any
    environment {
        // Read Credential config
        // CREDENTIAL_VAR=credentials('CREDENTIAL_CONFIG')

    }
    stages {
        stage('Prepare') {
            steps {
                script {
                    // Step Script here
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    // Step Script here
                }
            }
        }
        stage('Deploy Staging') {
            when {
                beforeAgent true
                branch 'qa'
            }
            parallel {
                stage('QA Server') {
                    steps {
                        script {
                            // Step Script here
                        }
                    }
                }
                stage('Staging Server') {
                    steps {
                        script {
                            // Step Script here
                        }
                    }
                }
            }
        }
        stage('Release Production') {
            when {
                beforeAgent true
                buildingTag()
                tag pattern: "^[0-9.]+\$", comparator: "REGEXP"
            }
            steps {
                script {
                    // Step Script here
                }
            }
        }
    }
}
