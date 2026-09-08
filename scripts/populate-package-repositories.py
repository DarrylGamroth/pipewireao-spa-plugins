#!/usr/bin/env python3
"""Create local standalone package repositories from the umbrella repository."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.parent
OWNER = "DarrylGamroth"
SOURCE_REVISION = "8d2edcf"

COMMON_PATHS = [
    ".dockerignore",
    ".gitignore",
    "LICENSE",
    "include",
    "meson.build",
    "meson_options.txt",
    "packaging/containers/Dockerfile.deploy",
    "packaging/containers/apt-install.sh",
    "packaging/deb/build.py",
    "packaging/deb/copyright",
    "spa/plugins/genicam",
    "spa/plugins/image-frame.h",
    "spa/plugins/test-image-frame.c",
]

COMPONENT_PATHS = {
    "core": [
        "Cargo.lock",
        "Cargo.toml",
        "crates",
        "docs/queue.md",
        "scripts/build-cargo.py",
        "scripts/check-exports.py",
        "spa/plugins/discard",
        "spa/plugins/hermes-decoder",
        "spa/plugins/ndarray",
        "spa/plugins/nuvu",
        "spa/plugins/pyrtc",
        "src/modules/queue",
    ],
    "fits": ["spa/plugins/fits"],
    "aravis": ["scripts/run-aravis-fake-gv-isolated.py", "spa/plugins/aravis", "subprojects/aravis.wrap"],
    "imagestreamio": ["spa/plugins/imagestreamio"],
    "alpao": [
        "docs/alpao-capture-benchmark.md",
        "docs/schemas/alpao-normalized-actuator-command-1.md",
        "spa/plugins/alpao",
    ],
    "egrabber": [
        "docs/egrabber-clprotocol.md",
        "scripts/check-exports.py",
        "spa/plugins/egrabber",
    ],
    "bgapi2": ["spa/plugins/bgapi2"],
    "edtpdv": ["spa/plugins/edtpdv"],
    "flisdk": [
        "scripts/extract-flisdk.py",
        "spa/plugins/egrabber/clprotocol_control.cpp",
        "spa/plugins/egrabber/control_backend.hpp",
        "spa/plugins/egrabber/feature.cpp",
        "spa/plugins/egrabber/feature.hpp",
        "spa/plugins/flisdk",
    ],
    "andor3": ["scripts/prepare-andor3.py", "spa/plugins/andor3"],
    "hamamatsu": ["scripts/prepare-hamamatsu.py", "spa/plugins/hamamatsu"],
    "hermes": ["spa/plugins/hermes"],
}


def run(command: list[str], *, cwd: Path, check: bool = True) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return completed.stdout.strip()


def repository_name(component: str, package: str) -> str:
    if component == "core":
        return "pipewireao-spa-plugins-core"
    return package


def package_dockerfile(component: str, repository: str, requires_rust: bool) -> str:
    tools = [
        "build-essential",
        "ca-certificates",
        "dpkg-dev",
        "meson",
        "ninja-build",
        "pkg-config",
        "python3",
    ]
    if requires_rust:
        tools.extend(["cargo", "rustc"])
    tool_lines = (" " + "\\" + "\n      ").join(tools)
    pipewire_context = "COPY --from=pipewire-rs . /src/pipewire-rs\n" if requires_rust else ""
    cache_mounts = (
        "RUN --mount=type=cache,target=/root/.cargo/registry,sharing=locked "
        + "\\"
        + "\n    --mount=type=cache,target=/root/.cargo/git,sharing=locked "
        + "\\"
        + "\n    "
        if requires_rust
        else "RUN "
    )
    return f"""# syntax=docker/dockerfile:1.7

ARG BASE_IMAGE=debian:trixie
FROM ${{BASE_IMAGE}} AS build

COPY packaging/containers/apt-install.sh /usr/local/bin/pipewireao-apt-install

ARG APT_BUILD_PACKAGES=""
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \\
    --mount=type=secret,id=apt_sources \\
    --mount=type=secret,id=apt_auth \\
    --mount=type=secret,id=apt_keyring \\
    /usr/local/bin/pipewireao-apt-install \\
      {tool_lines} \\
      ${{APT_BUILD_PACKAGES}}

{pipewire_context}COPY . /src/{repository}
WORKDIR /src/{repository}

ARG COMPONENT={component}
ARG DEB_VERSION=""
ARG HOST_DEPENDENCY=""
ARG MAINTAINER=""
ARG EXTRA_DEPENDS_JSON="[]"
ARG LIBRARY_DIRS_JSON="[]"
ARG MESON_OPTIONS_JSON="[]"
ARG SOURCE_DATE_EPOCH=946684800
{cache_mounts}SOURCE_DATE_EPOCH="${{SOURCE_DATE_EPOCH}}" \\
    python3 packaging/deb/build.py \\
      --component "${{COMPONENT}}" \\
      --output-dir /out \\
      --version "${{DEB_VERSION}}" \\
      --host-dependency "${{HOST_DEPENDENCY}}" \\
      --maintainer "${{MAINTAINER}}" \\
      --extra-depends-json "${{EXTRA_DEPENDS_JSON}}" \\
      --library-dirs-json "${{LIBRARY_DIRS_JSON}}" \\
      --meson-options-json "${{MESON_OPTIONS_JSON}}"

FROM scratch AS packages
COPY --from=build /out/ /
"""


def bake_file(component: str, requires_rust: bool) -> str:
    contexts = (
        '  contexts = {\n    pipewire-rs = "../pipewire-rs"\n  }\n'
        if requires_rust
        else ""
    )
    return f'''variable "COMPONENT" {{
  default = "{component}"
}}

variable "APT_BUILD_PACKAGES" {{ default = "" }}
variable "APT_RUNTIME_PACKAGES" {{ default = "" }}
variable "HOST_DEPENDENCY" {{ default = "" }}
variable "MAINTAINER" {{ default = "" }}
variable "EXTRA_DEPENDS_JSON" {{ default = "[]" }}
variable "LIBRARY_DIRS_JSON" {{ default = "[]" }}
variable "MESON_OPTIONS_JSON" {{ default = "[]" }}
variable "DEB_VERSION" {{ default = "" }}

target "package-common" {{
  context    = "."
  dockerfile = "packaging/containers/Dockerfile.package"
  target     = "packages"
{contexts}  args = {{
    APT_BUILD_PACKAGES = APT_BUILD_PACKAGES
    COMPONENT          = COMPONENT
    DEB_VERSION        = DEB_VERSION
    EXTRA_DEPENDS_JSON = EXTRA_DEPENDS_JSON
    HOST_DEPENDENCY    = HOST_DEPENDENCY
    LIBRARY_DIRS_JSON  = LIBRARY_DIRS_JSON
    MAINTAINER         = MAINTAINER
    MESON_OPTIONS_JSON = MESON_OPTIONS_JSON
  }}
}}

target "debian-13-package" {{
  inherits = ["package-common"]
  args = {{ BASE_IMAGE = "debian:trixie" }}
  output = ["type=local,dest=dist/debian-13/${{COMPONENT}}"]
}}

target "ubuntu-26-04-package" {{
  inherits = ["package-common"]
  args = {{ BASE_IMAGE = "ubuntu:26.04" }}
  output = ["type=local,dest=dist/ubuntu-26.04/${{COMPONENT}}"]
}}

target "debian-13-deploy" {{
  context    = "."
  dockerfile = "packaging/containers/Dockerfile.deploy"
  target     = "runtime"
  contexts = {{ packages = "target:debian-13-package" }}
  args = {{
    APT_RUNTIME_PACKAGES = APT_RUNTIME_PACKAGES
    BASE_IMAGE           = "debian:trixie"
  }}
  tags = ["pipewireao-spa-${{COMPONENT}}:debian-13"]
}}

target "ubuntu-26-04-deploy" {{
  context    = "."
  dockerfile = "packaging/containers/Dockerfile.deploy"
  target     = "runtime"
  contexts = {{ packages = "target:ubuntu-26-04-package" }}
  args = {{
    APT_RUNTIME_PACKAGES = APT_RUNTIME_PACKAGES
    BASE_IMAGE           = "ubuntu:26.04"
  }}
  tags = ["pipewireao-spa-${{COMPONENT}}:ubuntu-26.04"]
}}

group "default" {{
  targets = ["debian-13-package", "ubuntu-26-04-package"]
}}
'''


def readme(component: str, repository: str, private_runtime: bool) -> str:
    privacy = (
        "\nThis repository is private because its build and runtime dependency chain may include proprietary SDK material. Do not commit SDK payloads, credentials, or license files.\n"
        if private_runtime
        else ""
    )
    return f"""# {repository}

Standalone source and Debian/Ubuntu packaging for the `{component}` PipeWireAO SPA component.

This repository was split from
[`pipewireao-spa-plugins`](https://github.com/{OWNER}/pipewireao-spa-plugins)
at commit `{SOURCE_REVISION}`. The common public headers continue to be released
as the `pipewireao-spa-plugins-dev` binary package from the core repository.
{privacy}
## Package build

Supply the PipeWireAO build dependency through `APT_BUILD_PACKAGES` and its
runtime package expression through `HOST_DEPENDENCY`:

```console
export APT_BUILD_PACKAGES='pipewire-ao-dev'
export HOST_DEPENDENCY='pipewire-ao (>= 1.7)'
export MAINTAINER='Deployment Team <packages@example.org>'
docker buildx bake debian-13-package
docker buildx bake ubuntu-26-04-package
```

Vendor repositories also require the SDK development package in
`APT_BUILD_PACKAGES` and the corresponding runtime package in
`EXTRA_DEPENDS_JSON`. Private APT sources and credentials are passed with the
BuildKit secrets `apt_sources`, `apt_auth`, and `apt_keyring`.
"""


def main() -> None:
    source_revision = run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT)
    if source_revision != SOURCE_REVISION:
        raise SystemExit(
            f"expected source revision {SOURCE_REVISION}, found {source_revision}; review the migration map"
        )
    manifest = json.loads((ROOT / "packaging/deb/components.json").read_text())
    for component, paths in COMPONENT_PATHS.items():
        package = manifest["components"][component]["package"]
        repository = repository_name(component, package)
        destination = PARENT / repository
        if destination.exists():
            raise SystemExit(f"destination already exists: {destination}")

        run(
            ["git", "clone", "--no-checkout", "--no-hardlinks", str(ROOT), str(destination)],
            cwd=PARENT,
        )
        run(["git", "read-tree", "--empty"], cwd=destination)
        for path in [*COMMON_PATHS, *paths]:
            run(["git", "checkout", "HEAD", "--", path], cwd=destination)

        selected = {component: manifest["components"][component]}
        if component == "core":
            selected["dev"] = manifest["components"]["dev"]
        component_manifest = {
            "feature_options": manifest["feature_options"],
            "components": selected,
        }
        (destination / "packaging/deb/components.json").write_text(
            json.dumps(component_manifest, indent=2) + "\n"
        )
        requires_rust = component == "core"
        (destination / "packaging/containers/Dockerfile.package").write_text(
            package_dockerfile(component, repository, requires_rust)
        )
        (destination / "docker-bake.hcl").write_text(
            bake_file(component, requires_rust)
        )
        private_runtime = bool(selected[component].get("private_runtime"))
        (destination / "README.md").write_text(
            readme(component, repository, private_runtime)
        )

        run(
            [
                "git",
                "remote",
                "set-url",
                "origin",
                f"git@github.com:{OWNER}/{repository}.git",
            ],
            cwd=destination,
        )
        run(["git", "add", "--all"], cwd=destination)
        run(
            ["git", "commit", "-m", f"Split {component} package from umbrella repository"],
            cwd=destination,
        )
        print(destination)


if __name__ == "__main__":
    main()
