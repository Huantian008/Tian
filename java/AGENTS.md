# Repository Guidelines

## Project Structure & Module Organization
The repository groups several standalone Java practice modules (`basics-test`, `exercise2`, `hello-intellij`, `javawork`, `oop-practice`, `study3/classwork`). Each module keeps sources in `src/`, writes compiled classes to `out/`, and organizes topics through subpackages such as `javawork/src/javawork3` or `basics-test/src/test`; align new folders with their package statements. Keep `module-info.java` entries minimal and treat every `out/` directory as disposable build output.

## Build, Test, and Development Commands
Install a current LTS JDK (17+ recommended) and run builds from the repository root. `pwsh ./run_all.ps1` is the canonical workflow: it cleans each module’s `out/`, compiles all `.java`, and runs representative entry points (for example, `java -cp out test.Employee` or `javawork.work3`). For module-level work, run `rm -rf out && mkdir out && javac -d out $(find src -name '*.java')` on Bash (or the PowerShell pipeline in the script) and execute individual classes with `java -cp out package.ClassName`. Document any new console prompts and add a matching invocation to the script so automation stays deterministic.

## Coding Style & Naming Conventions
Use 4-space indentation, one public class per file, `PascalCase` for types, `camelCase` for members, and lowercase package names. Favor standard-library collections/streams, and keep files focused enough to explain with a concise header comment describing the scenario. Place new exercises under topic folders (`javawork/src/javawork5/`, `oop-practice/src/test4/`) and run IntelliJ Reformat Code or `google-java-format` before committing.

## Testing Guidelines
Testing relies on console runners located in `basics-test/src/test`, `oop-practice/src/test`, and the various `javawork` packages; there is no JUnit harness yet. Create regression checks under a `test` package with descriptive names so they can be launched via `java -cp out test.ClassName`, and make their output describe both inputs and results. Whenever you add a runnable demo, extend `run_all.ps1` with its `java -cp` command plus any deterministic stdin it expects.

## Commit & Pull Request Guidelines
Existing history favors short, imperative subjects (“Move LeetCode sources into cpp folder”), so continue that tone and note the touched module upfront (`javawork: add StudentID validator`). Commits and PRs should state motivation, list the commands executed (`pwsh ./run_all.ps1`, targeted `java` runs), and link an issue when available. Include screenshots only when editing the `web/` subtree; for Java changes, paste the relevant console output to help reviewers reproduce results.

## Local Environment Snapshot (Windows)
Last verified: 2026-03-02

- JDK (default): `C:\Program Files\Eclipse Adoptium\jdk-21.0.10.7-hotspot`
- `JAVA_HOME` (User/Machine): `C:\Program Files\Eclipse Adoptium\jdk-21.0.10.7-hotspot`
- IntelliJ SDK in use: JDK `21` (JavaSDK)
- Extra JDK candidates:
  - `E:\work\Java` (Oracle JDK 23)
  - `E:\idea\IntelliJ IDEA 2025.2.1\jbr` (JBR 21)

- Tomcat (configured): `E:\work\Java\Tomcat\apache-tomcat-10.1.34-windows-x64\apache-tomcat-10.1.34`
- `CATALINA_HOME`/`CATALINA_BASE` (User): above path
- User PATH includes: `%CATALINA_HOME%\bin`
- Tomcat version check: `Apache Tomcat/10.1.34`

- Maven (configured): `E:\idea\IntelliJ IDEA 2025.2.1\plugins\maven\lib\maven3`
- `M2_HOME` (User): above path
- User PATH includes: `%M2_HOME%\bin`
- Maven version check: `Apache Maven 3.9.9`

### IntelliJ User Config Notes
- Config root: `C:\Users\y2003\AppData\Roaming\JetBrains\IntelliJIdea2025.2\options`
- Applied style close to VS Code:
  - Editor/Console/Terminal font: `Consolas`, size `14`, line spacing `1.2`
  - UI font: `Segoe UI`, size `13`
  - Dark theme enabled (`Darcula` / `JetBrainsDarkTheme`)
- Related files:
  - `editor-font.xml`
  - `console-font.xml`
  - `terminal-font.xml`
  - `ui.lnf.xml`
  - `other.xml`
  - `jdk.table.xml`
  - `project.default.xml`

### Session Bootstrap Commands
Run these first in a new session to confirm environment:

```powershell
java -version
javac -version
echo $env:JAVA_HOME
echo $env:CATALINA_HOME
echo $env:M2_HOME
mvn -v
```

If terminal variables are stale, reopen terminal/IDE once before troubleshooting.
