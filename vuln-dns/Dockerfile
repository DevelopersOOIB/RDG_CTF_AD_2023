FROM alpine:3.18

#COPY authorized_keys /root/.ssh/authorized_keys

RUN echo http://mirror.yandex.ru/mirrors/alpine/v3.18/main > /etc/apk/repositories; \
    echo http://mirror.yandex.ru/mirrors/alpine/v3.18/community >> /etc/apk/repositories

RUN apk --update upgrade && \
	apk add --no-cache bind && \
    rm -rf /var/cache/apk/*
	
ADD init.sh /init.sh
RUN chmod 750 /init.sh

VOLUME ["/etc/bind", "/var/log/named"]

EXPOSE 53/udp

WORKDIR /etc/bind

CMD ["/init.sh"]