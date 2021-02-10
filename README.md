# gn_build

A standalone version of the GN "//build" toolchains and configurations.

This repo is drawn from the [Chromium](https://github.com/chromium/chromium) project at git revision [a877c035d7](https://github.com/chromium/chromium/commit/a877c035d76d5c05967a580f59f858d4f1bf110d), and removed some code coupled with the Chromium project to make it work standalone.

The main purpose of starting this project is to use the perfect iOS/macOS template such as `ios_framework_bundle`, `mac_framework_bundle`.

## Contents

Core GN templates and configuration and core Python build scripts.

- `//build/config` - Common templates via `.gni` files.
- `//build/toolchain` - GN toolchain definitions.
- `Other .py files` - Some are used by GN/Ninja. Some by gclient hooks, some
   are just random utilities.

## Docs

- [Writing GN Templates](docs/writing_gn_templates.md)
- [Debugging Slow Builds](docs/debugging_slow_builds.md)
- [Mac Hermetic Toolchains](docs/mac_hermetic_toolchain.md)
- [Android Build Documentation](android/docs/README.md)
