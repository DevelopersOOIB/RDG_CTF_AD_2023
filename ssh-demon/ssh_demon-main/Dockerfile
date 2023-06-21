FROM ubuntu:22.04

COPY ./sshd/ /sshd/
COPY ./sshd_config /usr/local/etc/sshd_config
RUN useradd -ms /bin/bash -g root -G sudo -u 1000 Admin_test_user
RUN  echo 'Admin_test_user:nYokmAIEc#4LWKrev72' | chpasswd -c SHA256
RUN /sshd/ssh-keygen -A -v

ENTRYPOINT ["/sshd/sshd", "-D"]
