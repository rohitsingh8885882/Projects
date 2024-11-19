/claim #3180

# sbt-openapi-codegen

An SBT plugin for generating Scala code from OpenAPI specifications with support for automatic code generation on file changes.

## Features

- Automatic code generation on specification file changes
- Support for multiple OpenAPI specification files
- Configurable package prefix for generated code
- Global and file-specific OpenAPI configurations
- Built on top of the official OpenAPI Generator

## Installation

Add the following to your `project/plugins.sbt`:

```sbt
addSbtPlugin("com.example" % "sbt-openapi-codegen" % "0.1.0-SNAPSHOT")
```

## Usage

```sbt
lazy val root = (project in file("."))
  .settings(
    openApiWatchMode := true,  // Enable automatic generation on file changes
    openApiSpecPaths := Seq(   // Specify OpenAPI spec files
      file("api/petstore.yaml"),
      file("api/users.yaml")
    ),
    openApiPackagePrefix := "com.example.generated",  // Package prefix for generated code
    
    // Global configuration for all specifications
    openApiGlobalConfig := Some(ConfigFactory.parseString("""
      |additionalProperties:
      |  dateLibrary: java8
      |  supportAsync: true
      """.stripMargin)),
      
    // File-specific configurations
    openApiFileConfig := { filter =>
      if (filter.accept(file("api/petstore.yaml"))) {
        Some(ConfigFactory.parseString("""
          |additionalProperties:
          |  usePlayWS: true
          """.stripMargin))
      } else None
    }
  )
```

## Configuration

| Setting | Type | Description | Default |
|---------|------|-------------|---------|
| `openApiWatchMode` | `Boolean` | Enable automatic generation on file changes | `false` |
| `openApiSpecPaths` | `Seq[File]` | Paths to OpenAPI specification files | `Seq.empty` |
| `openApiPackagePrefix` | `String` | Package prefix for generated code | `"generated"` |
| `openApiGlobalConfig` | `Option[Config]` | Global OpenAPI configuration | `None` |
| `openApiFileConfig` | `FileFilter => Option[Config]` | File-specific OpenAPI configuration | `_ => None` |

## Tasks

- `openApiGenerate`: Manually trigger code generation from OpenAPI specs

# Projects
