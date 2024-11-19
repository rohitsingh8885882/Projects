lazy val root = (project in file("."))
  .settings(
    version := "0.1",
    scalaVersion := "2.13.10",
    openApiWatchMode := true,
    openApiSpecPaths := Seq(
      file("api/petstore.yaml"),
      file("api/users.yaml")
    ),
    openApiPackagePrefix := "com.example.generated",
    openApiGlobalConfig := Some(ConfigFactory.parseString("""
      |additionalProperties:
      |  dateLibrary: java8
      |  supportAsync: true
      """.stripMargin)),
    openApiFileConfig := { filter =>
      if (filter.accept(file("api/petstore.yaml"))) {
        Some(ConfigFactory.parseString("""
          |additionalProperties:
          |  usePlayWS: true
          """.stripMargin))
      } else None
    }
  )