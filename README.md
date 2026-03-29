# rules_verilog

[![BCR](https://img.shields.io/badge/BCR-rules_verilog-green?logo=bazel)](https://registry.bazel.build/modules/rules_verilog)
[![CI](https://github.com/MrAMS/bazel_rules_verilog/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/MrAMS/bazel_rules_verilog/actions/workflows/ci.yml)

The primary goal of `rules_verilog` is to provide only the most **foundational** verilog/systemverilog interfaces (e.g., `verilog_library`).

> [!TIP]
>
> How this is different from https://github.com/hdl/bazel_rules_hdl? Why your repository basically only has one rule and a couple of providers?
>
> Please check https://github.com/bazelbuild/bazel-central-registry/pull/7852 and https://github.com/MrAMS/bazel_rules_verilog/issues/1 for more details

## What This Module Does

`verilog_library` collects:

- `srcs` (`.v`, `.sv`) — Verilog/SystemVerilog source files
- `hdrs` (`.vh`, `.svh`) — Verilog/SystemVerilog header files
- `includes` — include search paths (auto-derived from `hdrs` locations + explicit paths)
- `data` — data files needed during compilation or simulation
- `deps` — other `verilog_library` targets
- `top_module` — the local top module of this library (optional; empty string means "unspecified")
- `standard` — Verilog/SystemVerilog standard version (optional; empty string means "unspecified")

and propagates a transitive `VerilogInfo` provider that downstream rules can consume, like [rules_verilator](https://github.com/MrAMS/bazel_rules_verilator) and [rules_vivado](https://github.com/CruxML/bazel_rules_vivado).

## Installation (Bzlmod)

Add to `MODULE.bazel`:

```starlark
bazel_dep(name = "rules_verilog", version = "1.1.1")
```

## Usage

```starlark
load("@rules_verilog//verilog:defs.bzl", "verilog_library")

verilog_library(
    name = "core",
    srcs = ["core.sv"],
    hdrs = ["core_defines.svh"],
    standard = "2012",
)

verilog_library(
    name = "bus_headers",
    hdrs = ["axi_params.svh"],
    includes = ["include/bus"], # Explicitly add to include search paths
)

verilog_library(
    name = "soc",
    srcs = ["soc_top.sv"],
    deps = [
        ":core",
        ":bus_headers",
    ],
    data = ["rom_init.hex"], # Data files needed for simulation/compilation
    top_module = "soc_top",  # Specifies the local top module name of soc for downstream rules
)
```

`VerilogInfo` is exported from `@rules_verilog//verilog:defs.bzl` for custom rule authors.

## Development

Run all checks locally:

```bash
bazel test //...
```

## License

Apache-2.0.
