# --- build stage: compile the Spring Boot fat jar with Maven on JDK 21 ---
# Temurin-based image so it has both amd64 and arm64 (Apple Silicon) variants.
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app
COPY pom.xml ./
COPY src ./src
RUN mvn -B -q clean package -DskipTests

# --- runtime stage: slim JRE that just runs the jar ---
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /app/target/so-rest-api-3.0.2.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
