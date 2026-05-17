---
title: lpp (Loci Preprocessor)
category: Loci Source Language
status: complete
audience: both
attribution: llm
reviewed: false
---

# lpp — The Loci Preprocessor

**`lpp`** is the Loci source-language preprocessor. It translates `.loci` source
files — which contain Loci-specific directives (`$rule`, `$type`, `$include`) mixed
with ordinary C++ — into valid `.cc` C++ files that can be compiled with a standard
C++ compiler.

`lpp` is a source-to-source translator. It knows nothing about scheduling,
parallelism, or execution. Its sole job is to expand Loci syntax into the C++
class definitions and rule-registration calls that the runtime expects.

---

## Compilation Workflow

A typical Loci build compiles each `.loci` file in two stages:

```
foo.loci  ──lpp──>  foo.cc  ──g++──>  foo.o
```

In practice the build system (e.g., Loci's provided `Makefile` infrastructure)
handles this automatically. To invoke `lpp` directly:

```bash
lpp -I<include-dir> foo.loci -o foo.cc
```

If `-o` is omitted, generated C++ is written to standard output.

---

## Command-Line Flags

| Flag | Effect |
|------|--------|
| `-I<dir>` | Add `<dir>` to the `$include` search path. May be repeated. |
| `-o <file>` | Write generated C++ to `<file>` instead of stdout. |
| `-p` | **Pretty-print mode.** Suppresses `#line` directives. Produces readable output suitable for inspecting generated code. |
| `-D<var>[=<val>]` | Define a system variable (analogous to the C preprocessor `-D`). |
| `-v` / `-V` | Print the `lpp` version string and exit. |
| `-t` | Test-parse only; produce no output. Useful for syntax checking. |

### Pretty-Print Mode (`-p`)

By default, `lpp` inserts `#line` directives into the output so that C++ compiler
errors and debugger symbols point back to the original `.loci` source file and line.
This is the right mode for production builds.

For inspecting what `lpp` actually generated — for example, to understand how a
`$rule` was translated — use `-p` to get clean, uncluttered C++:

```bash
lpp -p foo.loci
```

---

## What lpp Translates

### `$rule` directives

Each `$rule` block is translated into a C++ class with:
- the rule's input/output/constraint/conditional metadata encoded as member
  function declarations
- the kernel body (the `compute` block) preserved as the `calculate()` method
- a static registration object that enrols the class in the global rule list at
  program startup

The rule type (`pointwise`, `singleton`, `unit`, `apply`, `default`, `optional`)
determines the generated base class.

### `$varName` access syntax

Within kernel bodies, every variable prefixed with `$` is expanded to the
appropriate C++ accessor expression for that variable's container type:

| Source syntax | Generated accessor |
|---|---|
| `$storeName` | read/write access to the current entity's value |
| `*$paramName` | dereference of the `param` (required in `prelude` blocks) |
| `$mapName->$target` | navigation through a `Map` to a related entity's value |
| `$storeVecName[i]` | element access for `storeVec` |
| `$storeMat[r][c]` | element access for `storeMat` via `Mat<T>` flyweight |
| `$$n` | current loop iteration counter |

### `$type` declarations

`$type` lines are consumed by `lpp` for type information and are **not** emitted
in the output. Their sole effect is to tell `lpp` which container type each variable
has, enabling correct accessor-code generation for every rule that references it.

### `$include` directives

`$include "header.lh"` is resolved by `lpp` against the search path built from
`-I` flags. The contents of the `.lh` file are read and processed inline. `$type`
declarations from included files are not re-emitted in the output.

### `$[Once]` blocks

Code inside a `$[Once] { ... }` block is emitted only once per translation unit,
regardless of how many times the enclosing header is included. See
[[source-language/dollar-once|$[Once]]].

---

## File Naming Conventions

| Extension | Role |
|-----------|------|
| `.loci` | Loci source file; input to `lpp` |
| `.lh` | Loci header; contains `$type` declarations, shared via `$include` |
| `.cc` | Generated C++ output; input to the C++ compiler |

---

## What lpp Does Not Do

`lpp` is a syntactic translator only. It does not:
- analyse data dependencies between rules
- construct or validate execution schedules
- allocate storage in the fact database
- emit any MPI, OpenMP, or GPU-specific code

All of those responsibilities belong to the runtime.

---

*See also:* [[source-language/dollar-type|$type]],
[[source-language/dollar-include|$include]],
[[source-language/dollar-rule|$rule syntax]],
[[source-language/dollar-once|$[Once]]],
[[program-lifecycle/global-rule-list|global_rule_list]]
