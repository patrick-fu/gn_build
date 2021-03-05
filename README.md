# gn_build

A standalone version of the GN "//build" toolchains and configurations.

This repo is drawn from the [Chromium](https://github.com/chromium/chromium) project at git revision [a877c035d7](https://github.com/chromium/chromium/commit/a877c035d76d5c05967a580f59f858d4f1bf110d), **and removed some code coupled with the Chromium project to make it work standalone.**

> The main purpose of starting this project is to use the perfect iOS/macOS template such as `ios_framework_bundle`, `mac_framework_bundle`.

## Example demo

**[https://github.com/patrick-fu/gn_build_example](https://github.com/patrick-fu/gn_build_example)**

An example project which use this repo as a sub-module to demonstrates how to organize and build iOS/macOS shared framework (XCFramework) and static library with GN & Ninja.

## Contents

Core GN templates and configuration and core Python build scripts.

- `//build/config` - Common templates via `.gni` files.
- `//build/toolchain` - GN toolchain definitions.
- `Other .py files` - Some are used by GN/Ninja. Some by gclient hooks, some
   are just random utilities.

## Worked and well tested features

1. Templates

   - `ios_framework_bundle`, supports build complete code signed framework for device, simulator, mac-catalyst.

   - `mac_framework_bundle`, supports build complete mac framework which contains "Headers" and "Modules".

2. Toolchains

   - Default use local Xcode clang toolchains for building iOS/macOS library.

   - Default use local Android NDK toolchains for building Android native library.
      (Need to set `android_ndk_root` and `android_ndk_version` args with `gn gen --args`)

   - Default use local Visual Studio MSVC toolchains for building Windows library.
