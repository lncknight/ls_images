FROM openjdk:21-slim-buster

RUN apt update -y
RUN apt install wget unzip -y
RUN cd ~ 
     && wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.7.0.2747.zip
     && unzip sonar-scanner-cli-4.7.0.2747.zip 

RUN mv /root/sonar-scanner-4.7.0.2747 /root/sonar-scanner-cli
