sbtPlugin := true

name := "sbt-openapi-codegen"
organization := "com.example"
version := "0.1.0-SNAPSHOT"

libraryDependencies ++= Seq(
  "org.openapitools" % "openapi-generator" % "7.0.1",
  "com.typesafe" % "config" % "1.4.3",
  "io.circe" %% "circe-core" % "0.14.6",
  "io.circe" %% "circe-generic" % "0.14.6",
  "io.circe" %% "circe-parser" % "0.14.6"
)