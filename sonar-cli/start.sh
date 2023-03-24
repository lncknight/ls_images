#!/bin/bash
/root/sonar-scanner-cli/bin/sonar-scanner \
  -Dsonar.projectKey=$YOUR_PROJECT_KEY \
  -Dsonar.sources=/app/src \
  -Dsonar.host.url=$SONARQUBE_URL \
  -Dsonar.login=$TOKEN
