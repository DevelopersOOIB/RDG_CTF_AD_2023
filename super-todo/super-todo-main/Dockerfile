FROM openjdk:17-jdk-alpine

RUN apk update && apk add curl

COPY target/super-todo-0.0.1-SNAPSHOT.jar super-todo.jar
ENTRYPOINT ["java", "-jar", "super-todo.jar"]
