# PipeWireAO SPA plugins

The PipeWireAO SPA plugin family is split into independently buildable source
repositories. A deployment includes the core repository and only the device or
transport integrations it needs. This keeps unrelated SDKs out of the build
context and lets proprietary integrations remain private.

The repository boundary does not prescribe a packaging format. Each component
can be built and staged with Meson, copied into a container or system image, or
turned into a native operating-system package.

## Components

| Component | Purpose | External dependency | Visibility |
| --- | --- | --- | --- |
| [`core`](https://github.com/DarrylGamroth/pipewireao-spa-plugins-core) | SDK-independent plugins, transforms, decoders, queue module, and public development headers | None | Public |
| [`fits`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-fits) | FITS sequence and simulated camera source | CFITSIO | Public |
| [`aravis`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-aravis) | Experimental Aravis camera source | Aravis | Public |
| [`imagestreamio`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-imagestreamio) | ImageStreamIO shared-memory bridge | ImageStreamIO | Public |
| [`alpao`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-alpao) | ALPAO FGN command-normalization operator and deformable-mirror sink | ALPAO ASDK for the sink | Private |
| [`egrabber`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-egrabber) | Euresys eGrabber camera integration | Euresys eGrabber SDK | Private |
| [`bgapi2`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-bgapi2) | Baumer GAPI2 camera integration | Baumer GAPI SDK | Private |
| [`edtpdv`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-edtpdv) | EDT PDV camera integration | EDT PDV SDK | Private |
| [`flisdk`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-flisdk) | First Light Imaging camera integration | FliSdk; optional GenICam CLProtocol support | Private |
| [`andor3`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-andor3) | Andor SDK3 camera integration | Andor SDK3 | Private |
| [`hamamatsu`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-hamamatsu) | Hamamatsu DCAM camera integration | DCAM-API | Private |
| [`hermes`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-hermes) | MPD HERMES FrontPanel camera source | HERMES and FrontPanel SDKs | Private |

The common development headers are an output of `core`, not a separate source
repository. The SDK-independent HERMES decoder also remains in `core`; the
private HERMES repository contains only the SDK-backed source.

Machine-readable repository metadata is in
[`repositories.json`](repositories.json).

## Compose a deployment

Build `core` first, then build each selected integration against its installed
headers and PipeWireAO. Every component README documents its feature option and
external SDK requirements.

A normal Meson install can be staged without modifying the host:

```console
meson setup build --prefix=/usr [component-specific options]
meson compile -C build
DESTDIR="$PWD/stage" meson install -C build
```

The resulting `stage` tree can be copied into a target root filesystem,
container image, appliance build, or package assembly step.

Each source repository also contains Docker Bake targets for Debian- and
Ubuntu-based deployment images. Separate targets export `.deb` files when that
format is useful. Those recipes are deployment conveniences; they are not the
reason for, or a constraint on, the repository split. Debian-specific details
are documented in [`docs/debian-packaging.md`](docs/debian-packaging.md).

## CI and coverage

Line coverage at 90% or below fails GitHub CI. Coverage checks are optional for
merges to `main`. Core applies the threshold separately to native and Rust
coverage. GitHub Actions uses OIDC to upload the reports to Codecov.

Public repositories show live CI and coverage badges for `main`. Private
repositories use link badges that open the workflow or report for readers with
access. Each plugin README describes which mocks, simulators, or
SDK-independent code CI exercises.

CI uses the line counts in its coverage reports. Badge percentages can differ
because Codecov counts partially covered lines separately.
See [how Codecov calculates coverage](https://docs.codecov.com/docs/about-code-coverage).

The coverage measurements below are from local runs on Debian 13 on 2026-11-18.
Core's initial Rust measurement covered Cargo tests. The verified measurement
also includes Rust code exercised by the Meson SPA host tests.

| Component | CI | Codecov | Initial line coverage | Verified line coverage | Gate |
| --- | --- | --- | --- | --- | --- |
| Core | [![CI status][core-ci-badge]][core-ci] | [![Codecov coverage][core-coverage-badge]][core-coverage] | 80.38% native, 44.76% Rust | 90.43% native, 91.76% Rust | Pass |
| FITS | [![CI status][fits-ci-badge]][fits-ci] | [![Codecov coverage][fits-coverage-badge]][fits-coverage] | 82.31% | 90.18% | Pass |
| Aravis | [![CI status][aravis-ci-badge]][aravis-ci] | [![Codecov coverage][aravis-coverage-badge]][aravis-coverage] | 55.66% | 90.25% | Pass |
| ImageStreamIO | [![CI status][imagestreamio-ci-badge]][imagestreamio-ci] | [![Codecov coverage][imagestreamio-coverage-badge]][imagestreamio-coverage] | 63.39% | 91.84% | Pass |
| ALPAO | [![GitHub Actions][private-ci-badge]][alpao-ci] | [![Codecov][private-coverage-badge]][alpao-coverage] | 82.65% | 90.53% | Pass |
| eGrabber | [![GitHub Actions][private-ci-badge]][egrabber-ci] | [![Codecov][private-coverage-badge]][egrabber-coverage] | 94.47% | 94.47% | Pass |
| BGAPI2 | [![GitHub Actions][private-ci-badge]][bgapi2-ci] | [![Codecov][private-coverage-badge]][bgapi2-coverage] | 97.73% | 97.73% | Pass |
| EDT PDV | [![GitHub Actions][private-ci-badge]][edtpdv-ci] | [![Codecov][private-coverage-badge]][edtpdv-coverage] | 72.53% | 91.42% | Pass |
| FliSdk | [![GitHub Actions][private-ci-badge]][flisdk-ci] | [![Codecov][private-coverage-badge]][flisdk-coverage] | 74.71% | 90.61% | Pass |
| Andor SDK3 | [![GitHub Actions][private-ci-badge]][andor3-ci] | [![Codecov][private-coverage-badge]][andor3-coverage] | 69.49% | 90.13% | Pass |
| Hamamatsu DCAM | [![GitHub Actions][private-ci-badge]][hamamatsu-ci] | [![Codecov][private-coverage-badge]][hamamatsu-coverage] | 65.85% | 90.14% | Pass |
| HERMES | [![GitHub Actions][private-ci-badge]][hermes-ci] | [![Codecov][private-coverage-badge]][hermes-coverage] | 76.19% | 93.59% | Pass |
| [HEART](https://github.com/DarrylGamroth/pipewireao-spa-plugin-heart#ci-and-coverage) | [![GitHub Actions][private-ci-badge]][heart-ci] | [![Codecov][private-coverage-badge]][heart-coverage] | 79.97% | 90.39% | Pass |
| [Iris](https://github.com/DarrylGamroth/pipewireao-spa-plugin-iris#ci-and-coverage) | [![GitHub Actions][private-ci-badge]][iris-ci] | [![Codecov][private-coverage-badge]][iris-coverage] | 76.11% | 90.07% | Pass |

The native suites and Core's Rust suite passed locally. The table records
software coverage for the workflow configurations, including SDK-independent
tests for eGrabber and BGAPI2. SDK-backed paths require the corresponding
vendor dependencies and test fixtures to measure coverage.

[core-ci-badge]: https://github.com/DarrylGamroth/pipewireao-spa-plugins-core/actions/workflows/ci.yml/badge.svg?branch=main
[core-ci]: https://github.com/DarrylGamroth/pipewireao-spa-plugins-core/actions/workflows/ci.yml
[core-coverage-badge]: https://codecov.io/github/DarrylGamroth/pipewireao-spa-plugins-core/branch/main/graph/badge.svg
[core-coverage]: https://app.codecov.io/github/DarrylGamroth/pipewireao-spa-plugins-core
[fits-ci-badge]: https://github.com/DarrylGamroth/pipewireao-spa-plugin-fits/actions/workflows/ci.yml/badge.svg?branch=main
[fits-ci]: https://github.com/DarrylGamroth/pipewireao-spa-plugin-fits/actions/workflows/ci.yml
[fits-coverage-badge]: https://codecov.io/github/DarrylGamroth/pipewireao-spa-plugin-fits/branch/main/graph/badge.svg
[fits-coverage]: https://app.codecov.io/github/DarrylGamroth/pipewireao-spa-plugin-fits
[aravis-ci-badge]: https://github.com/DarrylGamroth/pipewireao-spa-plugin-aravis/actions/workflows/ci.yml/badge.svg?branch=main
[aravis-ci]: https://github.com/DarrylGamroth/pipewireao-spa-plugin-aravis/actions/workflows/ci.yml
[aravis-coverage-badge]: https://codecov.io/github/DarrylGamroth/pipewireao-spa-plugin-aravis/branch/main/graph/badge.svg
[aravis-coverage]: https://app.codecov.io/github/DarrylGamroth/pipewireao-spa-plugin-aravis
[imagestreamio-ci-badge]: https://github.com/DarrylGamroth/pipewireao-spa-plugin-imagestreamio/actions/workflows/ci.yml/badge.svg?branch=main
[imagestreamio-ci]: https://github.com/DarrylGamroth/pipewireao-spa-plugin-imagestreamio/actions/workflows/ci.yml
[imagestreamio-coverage-badge]: https://codecov.io/github/DarrylGamroth/pipewireao-spa-plugin-imagestreamio/branch/main/graph/badge.svg
[imagestreamio-coverage]: https://app.codecov.io/github/DarrylGamroth/pipewireao-spa-plugin-imagestreamio
[private-ci-badge]: https://img.shields.io/badge/CI-GitHub%20Actions-blue
[private-coverage-badge]: https://img.shields.io/badge/coverage-Codecov-blue
[alpao-ci]: https://github.com/DarrylGamroth/pipewireao-spa-plugin-alpao/actions/workflows/ci.yml
[alpao-coverage]: https://app.codecov.io/github/DarrylGamroth/pipewireao-spa-plugin-alpao
[egrabber-ci]: https://github.com/DarrylGamroth/pipewireao-spa-plugin-egrabber/actions/workflows/ci.yml
[egrabber-coverage]: https://app.codecov.io/github/DarrylGamroth/pipewireao-spa-plugin-egrabber
[bgapi2-ci]: https://github.com/DarrylGamroth/pipewireao-spa-plugin-bgapi2/actions/workflows/ci.yml
[bgapi2-coverage]: https://app.codecov.io/github/DarrylGamroth/pipewireao-spa-plugin-bgapi2
[edtpdv-ci]: https://github.com/DarrylGamroth/pipewireao-spa-plugin-edtpdv/actions/workflows/ci.yml
[edtpdv-coverage]: https://app.codecov.io/github/DarrylGamroth/pipewireao-spa-plugin-edtpdv
[flisdk-ci]: https://github.com/DarrylGamroth/pipewireao-spa-plugin-flisdk/actions/workflows/ci.yml
[flisdk-coverage]: https://app.codecov.io/github/DarrylGamroth/pipewireao-spa-plugin-flisdk
[andor3-ci]: https://github.com/DarrylGamroth/pipewireao-spa-plugin-andor3/actions/workflows/ci.yml
[andor3-coverage]: https://app.codecov.io/github/DarrylGamroth/pipewireao-spa-plugin-andor3
[hamamatsu-ci]: https://github.com/DarrylGamroth/pipewireao-spa-plugin-hamamatsu/actions/workflows/ci.yml
[hamamatsu-coverage]: https://app.codecov.io/github/DarrylGamroth/pipewireao-spa-plugin-hamamatsu
[hermes-ci]: https://github.com/DarrylGamroth/pipewireao-spa-plugin-hermes/actions/workflows/ci.yml
[hermes-coverage]: https://app.codecov.io/github/DarrylGamroth/pipewireao-spa-plugin-hermes
[heart-ci]: https://github.com/DarrylGamroth/pipewireao-spa-plugin-heart/actions/workflows/ci.yml
[heart-coverage]: https://app.codecov.io/github/DarrylGamroth/pipewireao-spa-plugin-heart
[iris-ci]: https://github.com/DarrylGamroth/pipewireao-spa-plugin-iris/actions/workflows/ci.yml
[iris-coverage]: https://app.codecov.io/github/DarrylGamroth/pipewireao-spa-plugin-iris

## History

The final combined source tree is preserved by the
`monorepo-final-2026-09-08` tag. The component repositories retain the earlier
history through umbrella commit `8d2edcf`.
