#!/usr/bin/env python3
"""
Angular 14 -> 18 migration orchestrator.

This script intentionally does not implement Angular codemods. It runs the
official Angular CLI migrations step by step and guards package.json so direct
non-Angular dependencies keep their original references.

Typical usage:
  python3 angular-14-to-18-migrator.py /path/to/angular-app --dry-run
  python3 angular-14-to-18-migrator.py /path/to/angular-app --yes

Standalone migration is enabled by default because Angular 18 projects commonly
use standalone APIs. Disable it with --standalone none when the app must keep
NgModules for now.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


PACKAGE_SECTIONS = (
    "dependencies",
    "devDependencies",
    "peerDependencies",
    "optionalDependencies",
)

LOCK_FILES = (
    "package-lock.json",
    "npm-shrinkwrap.json",
    "yarn.lock",
    "pnpm-lock.yaml",
)

BACKUP_FILES = (
    "package.json",
    "angular.json",
    "nx.json",
    ".browserslistrc",
    "browserslist",
    "tsconfig.json",
    "tsconfig.app.json",
    "tsconfig.spec.json",
)

ANGULAR_RELATED_PACKAGES = {
    "rxjs",
    "tslib",
    "typescript",
    "zone.js",
}

STANDALONE_FULL = (
    "convert-to-standalone",
    "prune-ng-modules",
    "standalone-bootstrap",
)


class MigrationError(RuntimeError):
    pass


@dataclass(frozen=True)
class Config:
    project: Path
    target_major: int
    package_manager: str
    standalone: str
    standalone_path: str
    allow_dirty: bool
    allow_no_git: bool
    allow_non_14: bool
    dry_run: bool
    yes: bool
    skip_install: bool
    skip_build: bool
    skip_tests: bool
    ng_force: bool
    include_angular_eslint: bool


class Logger:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, message: str = "") -> None:
        print(message)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(message + "\n")


def parse_args() -> Config:
    parser = argparse.ArgumentParser(
        description="Safely migrate an Angular 14 project to Angular 18.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("project", help="Angular project root")
    parser.add_argument("--target-major", type=int, default=18)
    parser.add_argument(
        "--package-manager",
        choices=("auto", "npm", "yarn", "pnpm"),
        default="auto",
    )
    parser.add_argument(
        "--standalone",
        choices=("none", "convert", "prune", "bootstrap", "full"),
        default="full",
        help="Run official standalone migration stages after Angular 18 update",
    )
    parser.add_argument(
        "--standalone-path",
        default="src",
        help="Path passed to @angular/core:standalone migration",
    )
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--allow-no-git", action="store_true")
    parser.add_argument("--allow-non-14", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--skip-install", action="store_true")
    parser.add_argument("--skip-build", action="store_true")
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("--ng-force", action="store_true")
    parser.add_argument(
        "--include-angular-eslint",
        action="store_true",
        help="Allow @angular-eslint/* direct refs to move with Angular",
    )
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    package_manager = (
        detect_package_manager(project)
        if args.package_manager == "auto"
        else args.package_manager
    )
    return Config(
        project=project,
        target_major=args.target_major,
        package_manager=package_manager,
        standalone=args.standalone,
        standalone_path=args.standalone_path,
        allow_dirty=args.allow_dirty,
        allow_no_git=args.allow_no_git,
        allow_non_14=args.allow_non_14,
        dry_run=args.dry_run,
        yes=args.yes,
        skip_install=args.skip_install,
        skip_build=args.skip_build,
        skip_tests=args.skip_tests,
        ng_force=args.ng_force,
        include_angular_eslint=args.include_angular_eslint,
    )


def detect_package_manager(project: Path) -> str:
    if (project / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (project / "yarn.lock").exists():
        return "yarn"
    return "npm"


def load_package_json(project: Path) -> dict:
    package_json = project / "package.json"
    if not package_json.exists():
        raise MigrationError(f"package.json not found: {package_json}")
    return json.loads(package_json.read_text(encoding="utf-8"))


def save_package_json(project: Path, data: dict) -> None:
    (project / "package.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def all_direct_deps(package_json: dict) -> dict[str, str]:
    deps: dict[str, str] = {}
    for section in PACKAGE_SECTIONS:
        deps.update(package_json.get(section, {}))
    return deps


def find_dep(package_json: dict, name: str) -> str | None:
    for section in PACKAGE_SECTIONS:
        value = package_json.get(section, {}).get(name)
        if value:
            return value
    return None


def parse_major(version_spec: str) -> int | None:
    match = re.search(r"(\d+)(?:\.\d+)?(?:\.\d+)?", version_spec)
    return int(match.group(1)) if match else None


def is_git_repo(project: Path) -> bool:
    return (project / ".git").exists() or run_git(
        project, ("rev-parse", "--is-inside-work-tree"), check=False
    ).returncode == 0


def git_dirty(project: Path) -> bool:
    result = run_git(project, ("status", "--porcelain"), check=True)
    return bool(result.stdout.strip())


def run_git(project: Path, args: Sequence[str], check: bool) -> subprocess.CompletedProcess:
    return subprocess.run(
        ("git", *args),
        cwd=project,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def ensure_preflight(config: Config, package_json: dict, log: Logger) -> None:
    if not config.project.exists():
        raise MigrationError(f"Project path not found: {config.project}")
    if not (config.project / "angular.json").exists():
        raise MigrationError("angular.json not found. This does not look like an Angular CLI workspace.")

    current_spec = find_dep(package_json, "@angular/core")
    if not current_spec:
        raise MigrationError("@angular/core not found in package.json.")
    current_major = parse_major(current_spec)
    if current_major is None:
        raise MigrationError(f"Could not parse @angular/core version: {current_spec}")
    if current_major > config.target_major:
        raise MigrationError(f"Current Angular major is {current_major}, target is {config.target_major}.")
    if current_major != 14 and not config.allow_non_14:
        raise MigrationError(
            f"Expected Angular 14, found {current_spec}. Use --allow-non-14 to continue."
        )

    has_git = is_git_repo(config.project)
    if not has_git and not config.allow_no_git:
        raise MigrationError("Git repository not found. Use --allow-no-git if backup files are enough.")
    if has_git and git_dirty(config.project) and not config.allow_dirty:
        raise MigrationError("Git working tree is dirty. Commit/stash first or use --allow-dirty.")

    node_major, node_minor = node_version()
    if node_major < 18 or (node_major == 18 and node_minor < 19):
        raise MigrationError(
            f"Node {node_major}.{node_minor} is too old for Angular 18. Use Node >= 18.19."
        )

    log.write(f"Project: {config.project}")
    log.write(f"Package manager: {config.package_manager}")
    log.write(f"Angular current: {current_spec}")
    log.write(f"Angular target: {config.target_major}")
    log.write(f"Standalone migration: {config.standalone}")


def node_version() -> tuple[int, int]:
    result = subprocess.run(
        ("node", "--version"),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    match = re.search(r"v(\d+)\.(\d+)", result.stdout.strip())
    if not match:
        raise MigrationError(f"Could not parse Node version: {result.stdout.strip()}")
    return int(match.group(1)), int(match.group(2))


def make_backup(project: Path, timestamp: str, log: Logger, dry_run: bool) -> Path:
    backup_dir = project / ".angular-migration-backups" / timestamp
    log.write(f"Backup: {backup_dir}")
    if dry_run:
        return backup_dir
    backup_dir.mkdir(parents=True, exist_ok=True)
    for name in (*BACKUP_FILES, *LOCK_FILES):
        src = project / name
        if src.exists():
            dst = backup_dir / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    return backup_dir


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def ensure_tools(config: Config) -> None:
    for tool in ("node", "npx", config.package_manager):
        if not command_exists(tool):
            raise MigrationError(f"Required command not found on PATH: {tool}")


def run_cmd(
    cmd: Sequence[str],
    config: Config,
    log: Logger,
    env_extra: dict[str, str] | None = None,
) -> None:
    rendered = " ".join(cmd)
    log.write(f"$ {rendered}")
    if config.dry_run:
        return

    env = os.environ.copy()
    env.update(
        {
            "CI": "true",
            "NG_DISABLE_VERSION_CHECK": "1",
        }
    )
    if env_extra:
        env.update(env_extra)

    process = subprocess.Popen(
        cmd,
        cwd=config.project,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
    )
    assert process.stdout is not None
    for line in process.stdout:
        log.write(line.rstrip())
    if process.wait() != 0:
        raise MigrationError(f"Command failed: {rendered}")


def install_cmd(package_manager: str) -> tuple[str, ...]:
    if package_manager == "npm":
        return ("npm", "install")
    if package_manager == "yarn":
        return ("yarn", "install")
    if package_manager == "pnpm":
        return ("pnpm", "install")
    raise MigrationError(f"Unsupported package manager: {package_manager}")


def run_script_cmd(package_manager: str, script: str) -> tuple[str, ...]:
    if package_manager == "npm":
        return ("npm", "run", script)
    if package_manager == "yarn":
        return ("yarn", script)
    if package_manager == "pnpm":
        return ("pnpm", script)
    raise MigrationError(f"Unsupported package manager: {package_manager}")


def angular_cli_cmd(major: int, *args: str) -> tuple[str, ...]:
    return ("npx", "-y", f"@angular/cli@{major}", *args)


def ng_update_cmd(major: int, package_json: dict, config: Config) -> tuple[str, ...]:
    packages = [f"@angular/core@{major}", f"@angular/cli@{major}"]
    if find_dep(package_json, "@angular/material"):
        packages.append(f"@angular/material@{major}")
    elif find_dep(package_json, "@angular/cdk"):
        packages.append(f"@angular/cdk@{major}")

    args = ["update", *packages, "--allow-dirty"]
    if config.ng_force:
        args.append("--force")
    return angular_cli_cmd(major, *args)


def is_angular_related(name: str, include_angular_eslint: bool) -> bool:
    if name.startswith("@angular/") or name.startswith("@angular-devkit/"):
        return True
    if include_angular_eslint and name.startswith("@angular-eslint/"):
        return True
    return name in ANGULAR_RELATED_PACKAGES


def restore_non_angular_refs(
    project: Path,
    original: dict,
    include_angular_eslint: bool,
    log: Logger,
    dry_run: bool,
) -> list[str]:
    current = load_package_json(project)
    restored: list[str] = []

    for section in PACKAGE_SECTIONS:
        original_deps = original.get(section, {})
        current_deps = current.get(section, {})
        for name, original_ref in original_deps.items():
            if name not in current_deps:
                continue
            if is_angular_related(name, include_angular_eslint):
                continue
            if current_deps[name] != original_ref:
                restored.append(f"{section}:{name} {current_deps[name]} -> {original_ref}")
                current_deps[name] = original_ref

    if restored:
        log.write("Restoring non-Angular direct references:")
        for item in restored:
            log.write(f"  - {item}")
        if not dry_run:
            save_package_json(project, current)
    return restored


def build_if_available(config: Config, package_json: dict, log: Logger) -> None:
    if config.skip_build:
        return
    scripts = package_json.get("scripts", {})
    if "build" in scripts:
        run_cmd(run_script_cmd(config.package_manager, "build"), config, log)
    else:
        run_cmd(angular_cli_cmd(config.target_major, "build"), config, log)


def test_if_available(config: Config, package_json: dict, log: Logger) -> None:
    if config.skip_tests:
        return
    scripts = package_json.get("scripts", {})
    if "test" in scripts:
        run_cmd(run_script_cmd(config.package_manager, "test"), config, log)


def standalone_modes(value: str) -> tuple[str, ...]:
    if value == "none":
        return ()
    if value == "convert":
        return ("convert-to-standalone",)
    if value == "prune":
        return ("prune-ng-modules",)
    if value == "bootstrap":
        return ("standalone-bootstrap",)
    return STANDALONE_FULL


def run_standalone_migration(config: Config, log: Logger) -> None:
    for mode in standalone_modes(config.standalone):
        run_cmd(
            angular_cli_cmd(
                config.target_major,
                "generate",
                "@angular/core:standalone",
                f"--mode={mode}",
                f"--path={config.standalone_path}",
                "--defaults",
            ),
            config,
            log,
        )
        package_json = load_package_json(config.project)
        build_if_available(config, package_json, log)


def write_report(
    project: Path,
    timestamp: str,
    before: dict,
    after: dict,
    backup_dir: Path,
    log_path: Path,
    dry_run: bool,
) -> Path:
    report = project / f"angular-14-to-18-migration-report-{timestamp}.md"
    before_deps = all_direct_deps(before)
    after_deps = all_direct_deps(after)
    changed = [
        (name, before_deps.get(name), after_ref)
        for name, after_ref in sorted(after_deps.items())
        if before_deps.get(name) != after_ref
    ]

    lines = [
        "# Angular 14 to 18 migration report",
        "",
        f"- Generated at: {timestamp}",
        f"- Backup: `{backup_dir}`",
        f"- Log: `{log_path}`",
        f"- Dry run: `{dry_run}`",
        "",
        "## Changed direct package references",
        "",
    ]
    if changed:
        for name, old, new in changed:
            lines.append(f"- `{name}`: `{old}` -> `{new}`")
    else:
        lines.append("- No direct package reference changes detected.")
    lines.extend(
        [
            "",
            "## Manual checks",
            "",
            "- Review standalone migration changes, especially routes, providers, forRoot/forChild patterns, and lazy modules.",
            "- Review any test modules that still depend on removed NgModules.",
            "- Run the application locally and verify critical flows.",
        ]
    )

    if not dry_run:
        report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def confirm_or_exit(config: Config, log: Logger) -> None:
    if config.dry_run or config.yes:
        return
    log.write("This will modify the Angular project. Re-run with --yes to continue.")
    raise SystemExit(2)


def migrate(config: Config, log: Logger) -> None:
    ensure_tools(config)
    original = load_package_json(config.project)
    ensure_preflight(config, original, log)
    confirm_or_exit(config, log)

    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = make_backup(config.project, timestamp, log, config.dry_run)
    current_major = parse_major(find_dep(original, "@angular/core") or "")
    assert current_major is not None

    if not config.skip_install:
        run_cmd(install_cmd(config.package_manager), config, log)

    for major in range(current_major + 1, config.target_major + 1):
        package_json = load_package_json(config.project)
        run_cmd(ng_update_cmd(major, package_json, config), config, log)
        restore_non_angular_refs(
            config.project,
            original,
            config.include_angular_eslint,
            log,
            config.dry_run,
        )
        if not config.skip_install:
            run_cmd(install_cmd(config.package_manager), config, log)
        build_if_available(config, load_package_json(config.project), log)

    run_standalone_migration(config, log)
    final_package_json = load_package_json(config.project)
    test_if_available(config, final_package_json, log)

    report = write_report(
        config.project,
        timestamp,
        original,
        final_package_json,
        backup_dir,
        log.path,
        config.dry_run,
    )
    log.write(f"Report: {report}")
    log.write("Done.")


def main() -> int:
    config = parse_args()
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log = Logger(config.project / ".angular-migration-logs" / f"{timestamp}.log")
    try:
        migrate(config, log)
        return 0
    except MigrationError as exc:
        log.write(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
