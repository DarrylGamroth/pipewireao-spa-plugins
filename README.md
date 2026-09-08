# PipeWireAO SPA plugin repositories

This repository is the architecture, release, and migration index for the
PipeWireAO SPA plugin family. Component source moved to independently buildable
repositories on 2026-09-08.

The final combined source tree is retained at the annotated tag
`monorepo-final-2026-09-08`. Each component repository preserves history through
umbrella commit `8d2edcf` and adds one split commit containing its standalone
build and packaging configuration.

## Repositories

| Component | Source repository | Visibility | Binary packages |
| --- | --- | --- | --- |
| Core | [`pipewireao-spa-plugins-core`](https://github.com/DarrylGamroth/pipewireao-spa-plugins-core) | Public | `pipewireao-spa-plugins-core`, `pipewireao-spa-plugins-dev` |
| FITS | [`pipewireao-spa-plugin-fits`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-fits) | Public | `pipewireao-spa-plugin-fits` |
| Aravis | [`pipewireao-spa-plugin-aravis`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-aravis) | Public | `pipewireao-spa-plugin-aravis` |
| ImageStreamIO | [`pipewireao-spa-plugin-imagestreamio`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-imagestreamio) | Public | `pipewireao-spa-plugin-imagestreamio` |
| ALPAO | [`pipewireao-spa-plugin-alpao`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-alpao) | Private | `pipewireao-spa-plugin-alpao` |
| Euresys eGrabber | [`pipewireao-spa-plugin-egrabber`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-egrabber) | Private | `pipewireao-spa-plugin-egrabber` |
| Baumer GAPI2 | [`pipewireao-spa-plugin-bgapi2`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-bgapi2) | Private | `pipewireao-spa-plugin-bgapi2` |
| EDT PDV | [`pipewireao-spa-plugin-edtpdv`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-edtpdv) | Private | `pipewireao-spa-plugin-edtpdv` |
| First Light Imaging FliSdk | [`pipewireao-spa-plugin-flisdk`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-flisdk) | Private | `pipewireao-spa-plugin-flisdk` |
| Andor SDK3 | [`pipewireao-spa-plugin-andor3`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-andor3) | Private | `pipewireao-spa-plugin-andor3` |
| Hamamatsu DCAM-API | [`pipewireao-spa-plugin-hamamatsu`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-hamamatsu) | Private | `pipewireao-spa-plugin-hamamatsu` |
| MPD HERMES | [`pipewireao-spa-plugin-hermes`](https://github.com/DarrylGamroth/pipewireao-spa-plugin-hermes) | Private | `pipewireao-spa-plugin-hermes` |

The development headers are a binary output of the core source repository; they
do not have a separate GitHub repository. The ALPAO repository owns both the FGN
command-normalization operator and the ASDK-backed deformable-mirror sink. The
SDK-independent HERMES decoder remains in core.

Machine-readable repository and package metadata is in
[`repositories.json`](repositories.json). Packaging conventions and the private
APT boundary remain documented in
[`docs/debian-packaging.md`](docs/debian-packaging.md).
