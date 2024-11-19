import sbt._
import sbt.Keys._
import scala.collection.JavaConverters._
import com.typesafe.config.{Config, ConfigFactory}

object OpenApiCodegenPlugin extends AutoPlugin {
  object autoImport {
    val openApiGenerate = taskKey[Unit]("Generate code from OpenAPI specs")
    val openApiWatchMode = settingKey[Boolean]("Enable automatic generation on file changes")
    val openApiSpecPaths = settingKey[Seq[File]]("Paths to OpenAPI specification files")
    val openApiPackagePrefix = settingKey[String]("Package prefix for generated code")
    val openApiGlobalConfig = settingKey[Option[Config]]("Global OpenAPI configuration")
    val openApiFileConfig = settingKey[FileFilter => Option[Config]]("File-specific OpenAPI configuration")
  }

  import autoImport._

  override def trigger = allRequirements

  override lazy val projectSettings = Seq(
    openApiWatchMode := false,
    openApiSpecPaths := Seq.empty,
    openApiPackagePrefix := "generated",
    openApiGlobalConfig := None,
    openApiFileConfig := (_ => None),

    openApiGenerate := {
      val log = streams.value.log
      val specs = openApiSpecPaths.value
      val packagePrefix = openApiPackagePrefix.value
      val globalConfig = openApiGlobalConfig.value
      val fileConfigFn = openApiFileConfig.value

      specs.foreach { specFile =>
        log.info(s"Generating code from ${specFile.getName}")
        generateCode(
          specFile,
          packagePrefix,
          globalConfig,
          fileConfigFn(new SimpleFileFilter(_.getAbsolutePath == specFile.getAbsolutePath))
        )
      }
    },

    watchSources ++= {
      if (openApiWatchMode.value) {
        openApiSpecPaths.value.map(WatchSource(_))
      } else {
        Seq.empty
      }
    }
  )

  private def generateCode(
    specFile: File,
    packagePrefix: String,
    globalConfig: Option[Config],
    fileConfig: Option[Config]
  ): Unit = {
    import org.openapitools.codegen.{CodegenConfig, DefaultGenerator, Generator}
    import org.openapitools.codegen.config.{CodegenConfigurator, GeneratorProperties}

    val configurator = new CodegenConfigurator()
    configurator.setInputSpec(specFile.getAbsolutePath)
    configurator.setOutputDir("target/generated-sources/openapi")
    configurator.setPackageName(s"$packagePrefix.${specFile.getName.split("\\.")(0)}")
    configurator.setGeneratorName("scala-akka")

    // Apply global config
    globalConfig.foreach { config =>
      config.entrySet().asScala.foreach { entry =>
        configurator.addAdditionalProperty(entry.getKey, entry.getValue.unwrapped())
      }
    }

    // Apply file-specific config
    fileConfig.foreach { config =>
      config.entrySet().asScala.foreach { entry =>
        configurator.addAdditionalProperty(entry.getKey, entry.getValue.unwrapped())
      }
    }

    val generator = new DefaultGenerator()
    generator.opts(configurator.toClientOptInput()).generate()
  }
}