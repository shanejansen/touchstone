FROM openjdk:8-jre-alpine
WORKDIR /app
COPY target/demo-1.0.jar .
EXPOSE 8080
ENV SPRING_PROFILES_ACTIVE touchstone
CMD java -jar ./demo-1.0.jar
