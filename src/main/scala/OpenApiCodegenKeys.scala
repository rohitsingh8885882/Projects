import sbt._

trait OpenApiCodegenKeys {
  val openApiGenerate = taskKey[Unit]("Generate code from OpenAPI specs")
  val openApiWatchMode = settingKey[Boolean]("Enable automatic generation on file changes")
  val openApiSpecPaths = settingKey[Seq[File]]("Paths to OpenAPI specification files")
  val openApiPackagePrefix = settingKey[String]("Package prefix for generated code")
  val openApiGlobalConfig = settingKey[Option[com.typesafe.config.Config]]("Global OpenAPI configuration")
  val openApiFileConfig = settingKey[FileFilter => Option[com.typesafe.config.Config]]("File-specific OpenAPI configuration")
}