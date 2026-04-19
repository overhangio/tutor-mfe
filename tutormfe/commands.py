from __future__ import annotations

import json
import os
import shutil
import tempfile

import click
from tutor import env, exceptions, fmt, images
from tutor.commands.context import Context


@click.group(name="mfe", help="Commands for the MFE plugin.")
def mfe_command() -> None:
    pass


@mfe_command.command(
    name="update-site-lockfile",
    help=(
        "Regenerate the frontend-base site's package-lock.json with the latest "
        "versions allowed by the declared semver ranges. Requires `tutor config "
        "save` to have been run first."
    ),
)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, writable=True, resolve_path=True),
    default="package-lock.json",
    show_default=True,
    help="Path to write the refreshed lockfile to.",
)
@click.option(
    "--scope",
    "scopes",
    multiple=True,
    help=(
        "npm scope prefix to limit updates to (e.g. '@openedx/'). May be "
        "passed multiple times. If neither --scope nor --package is given, "
        "all dependencies are updated."
    ),
)
@click.option(
    "--package",
    "packages",
    multiple=True,
    help=(
        "Exact package name to update. May be passed multiple times and "
        "combined with --scope."
    ),
)
@click.pass_obj
def update_site_lockfile(
    context: Context,
    output: str,
    scopes: tuple[str, ...],
    packages: tuple[str, ...],
) -> None:
    build_path = env.pathjoin(context.root, "plugins", "mfe", "build", "mfe")
    if not os.path.isdir(build_path):
        raise exceptions.TutorError(
            f"Rendered MFE build directory not found at {build_path}. "
            "Run `tutor config save` first."
        )
    selected = _resolve_packages(build_path, scopes, packages)
    with tempfile.TemporaryDirectory() as tmp:
        images.build(
            build_path,
            "tutor-mfe-lockfile:refresh",
            "--target=site-lockfile",
            "--no-cache-filter=site-lockfile-builder",
            f"--build-arg=NPM_UPDATE_PACKAGES={' '.join(selected)}",
            f"--output=type=local,dest={tmp}",
        )
        src = os.path.join(tmp, "package-lock.json")
        if not os.path.exists(src):
            raise exceptions.TutorError(
                "Docker build did not produce a package-lock.json. "
                "Ensure at least one frontend app is enabled via FRONTEND_APPS."
            )
        shutil.copy(src, output)
    fmt.echo_info(f"Refreshed lockfile written to {output}")


def _resolve_packages(
    build_path: str, scopes: tuple[str, ...], packages: tuple[str, ...]
) -> list[str]:
    if not scopes and not packages:
        return []
    pkg_path = os.path.join(build_path, "site", "package.json")
    try:
        with open(pkg_path, encoding="utf-8") as f:
            pkg = json.load(f)
    except FileNotFoundError as e:
        raise exceptions.TutorError(
            f"Rendered site package.json not found at {pkg_path}."
        ) from e
    declared = {
        *pkg.get("dependencies", {}).keys(),
        *pkg.get("devDependencies", {}).keys(),
    }
    selected = {
        name
        for name in declared
        if name in packages or any(name.startswith(s) for s in scopes)
    }
    if not selected:
        raise exceptions.TutorError(
            "No dependencies matched the given --scope / --package filters."
        )
    return sorted(selected)
