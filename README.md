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

## History

The final combined source tree is preserved by the
`monorepo-final-2026-09-08` tag. The component repositories retain the earlier
history through umbrella commit `8d2edcf`.
