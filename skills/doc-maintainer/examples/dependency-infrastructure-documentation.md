# Example: Dependency/Infrastructure Documentation

**Scenario**: Upgraded Spring Boot from 2.7 to 3.2, which changes the minimum Java version to 17, migrates `javax.*` imports to `jakarta.*`, and replaces the deprecated `spring.redis.*` config prefix with `spring.data.redis.*`

**Change Type**: Dependency/Infrastructure Change

**Documentation Updates**:

## 1. README.md

Updated prerequisites and setup sections:

```markdown
## Prerequisites

- **Java 17** or later (previously Java 11)
- Maven 3.8+
- Docker (for local Redis and database containers)

## Getting Started

```bash
./mvnw clean install
./mvnw spring-boot:run
```
```

## 2. docs/configuration.md

```markdown
## Redis Configuration

Configure the Redis connection using the `spring.data.redis` prefix (changed from `spring.redis` in Spring Boot 3.x):

```yaml
spring:
  data:
    redis:
      host: ${REDIS_HOST:localhost}
      port: ${REDIS_PORT:6379}
      password: ${REDIS_PASSWORD:}
```

> **Migration note**: If upgrading from Spring Boot 2.x, rename all `spring.redis.*` keys to `spring.data.redis.*` in your environment configuration and `.env` files.
```

## 3. CHANGELOG.md

```markdown
## [2.0.0] - 2026-04-30

### Changed
- Upgraded Spring Boot from 2.7 to 3.2 (#456)
- Minimum Java version raised to 17
- Migrated all `javax.*` imports to `jakarta.*`
- Redis config prefix changed from `spring.redis.*` to `spring.data.redis.*`

### Migration
See [docs/migration-2.x-to-3.x.md](docs/migration-2.x-to-3.x.md) for step-by-step upgrade instructions.
```

## 4. docs/migration-2.x-to-3.x.md (new file)

```markdown
# Migration Guide: Spring Boot 2.7 → 3.2

## Prerequisites
- Upgrade your local JDK to Java 17 before building.

## Step-by-step

### 1. Update Java version
In `pom.xml`, change:
```xml
<java.version>11</java.version>
```
to:
```xml
<java.version>17</java.version>
```

### 2. Rename Redis config keys
In all environment config files and `.env` templates, replace:
```
spring.redis.host=...
spring.redis.port=...
```
with:
```
spring.data.redis.host=...
spring.data.redis.port=...
```

### 3. Replace javax imports
Run a global find-and-replace across `src/`:
- `javax.persistence` → `jakarta.persistence`
- `javax.validation` → `jakarta.validation`
- `javax.servlet` → `jakarta.servlet`

### 4. Verify
```bash
./mvnw clean verify
```
```

## 5. docs/deployment.md

```markdown
## Runtime Requirements

| Requirement | Minimum version |
|---|---|
| Java | 17 |
| Spring Boot | 3.2 |
| Redis | 6.0 |

Ensure CI/CD pipelines and production container images use a Java 17 base image.
```

---

## Key Documentation Characteristics

- **Change Type**: Dependency/Infrastructure Change
- **Documentation Scope**: README, Configuration Guide, Changelog, Migration Guide, Deployment Docs
- **Primary Focus**: Version requirements, breaking configuration changes, and step-by-step migration path
- **Impact Level**: High (breaking changes affecting all environments and developers)
