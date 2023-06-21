from ubuntu:18.04
workdir /minecraft
run apt-get update && apt-get -y install openjdk-8-jre-headless
copy task/ .

entrypoint ["/bin/sh", "start.sh"]
