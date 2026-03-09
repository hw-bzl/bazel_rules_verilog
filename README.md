# rules_verilog

[![CI](https://github.com/MrAMS/bazel_rules_verilog/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/MrAMS/bazel_rules_verilog/actions/workflows/ci.yml)

A small Bazel module that provides reusable SystemVerilog/Verilog dependency graph metadata via `verilog_library`.

## What This Module Does

`verilog_library` collects:

- `srcs` (`.v`, `.sv`)
- `hdrs` (`.vh`, `.svh`)
- `data` (runtime/compile-side data files)
- `deps` (other `verilog_library` targets)

and propagates a transitive `VerilogInfo` provider that downstream rules can consume, like [rules_verilator](https://github.com/MrAMS/bazel_rules_verilator).

## Installation (Bzlmod)

Add to `MODULE.bazel`:

```starlark
bazel_dep(name = "rules_verilog", version = "0.1.0")
```

## Usage

```starlark
load("@rules_verilog//verilog:defs.bzl", "verilog_library")

verilog_library(
    name = "core",
    srcs = ["core.sv"],
    hdrs = ["core.svh"],
)

verilog_library(
    name = "soc",
    srcs = ["soc_top.sv"],
    deps = [":core"],
)
```

`VerilogInfo` and helper constructors are exported from `@rules_verilog//verilog:defs.bzl` for custom rule authors.

## Development

Run all checks locally:

```bash
bazel test //...
```

## License

Apache-2.0.
