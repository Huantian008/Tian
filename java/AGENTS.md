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
