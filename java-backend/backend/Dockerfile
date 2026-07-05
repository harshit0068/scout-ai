FROM eclipse-temurin:23-jdk AS build
WORKDIR /app
COPY java-backend/backend /app
RUN chmod +x gradlew
RUN ./gradlew build -x test

FROM eclipse-temurin:23-jre
WORKDIR /app
COPY --from=build /app/build/libs/*.jar app.jar
COPY leads.db /app/leads.db
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]