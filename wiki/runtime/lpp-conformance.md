---
title: lpp Conformance Obligations
category: Runtime Specification
status: normative
audience: runtime
---

# lpp Conformance Obligations

A conforming Loci preprocessor must translate each source construct in a `.loci` file
into C++ that satisfies the requirements stated in this page. The normative reference
implementation is `lpp` as shipped with `loci-4.1.2`.

## `$rule` Translation

For each `$rule ruleType(outputs <- inputs), ...` declaration, a conforming
preprocessor must generate:

1. A C++ class inheriting from the appropriate base class (see
   [[runtime/rule-class-interface|Rule Class Interface]]).
2. A constructor that calls `name_store`, `input`, `output`, `constraint`, and
   `conditional` for every variable and clause present in the rule signature.
3. A `calculate(Entity e)` method containing the compute-block body for per-entity
   rules, **or** a `compute(const sequence &seq)` method for rules with
   `option(disable_threading)` or that operate on singletons.
4. A `prelude(const sequence &seq)` method containing the prelude-block body, if a
   `prelude` block is present.
5. A file-scope `Loci::register_rule<ClassName>` object named uniquely within the
   translation unit.

## `$type` Translation

`$type` declarations are **not** emitted in the generated C++. They are consumed
internally by the preprocessor to determine which container handle type (`store<T>`,
`param<T>`, etc.) to use when generating member variable declarations inside rule
classes.

A conforming preprocessor must:
- Accept conflicting `$type` declarations for the same variable across translation
  units only if they agree on the container type; otherwise emit a diagnostic.
- Not emit any runtime registration or storage allocation for `$type` declarations.

## `$include` Translation

`$include "header.lh"` must be resolved against the search path supplied via `-I`
flags. The included file's contents are processed as if they appeared inline. `$type`
declarations from included files are consumed but not re-emitted, preventing
redeclaration errors when the same header is included from multiple translation units.

## `$$n` Access

The loop counter `$$n` is expanded to a `const_param<int>` named `$$n` in the
generated code. The preprocessor must generate the appropriate `name_store` call and
use the `*` dereference when accessing it in prelude blocks.

## `$[Once]` Blocks

Code inside `$[Once] { ... }` must be guarded against multiple emission when the
enclosing file is included more than once. The generated C++ must use a preprocessor
include guard or equivalent mechanism to ensure the block body appears exactly once
per translation unit.

## `#line` Directives

By default, the preprocessor must emit `#line` directives mapping generated C++ line
numbers back to the original `.loci` source file and line number. The `-p`
(pretty-print) flag suppresses all `#line` directives.

## Variable Access Expansion

Within compute and prelude blocks, every `$varName` must be expanded to the correct
C++ accessor expression for the variable's declared container type:

| Source expression | Container type | Generated C++ |
|---|---|---|
| `$store_var` | `store<T>` | `store_var[e]` (per-entity) |
| `*$param_var` | `param<T>` | `*(param_var)` |
| `$map->$target` | `Map` | `target[map[e]]` |
| `$mvec[i]` | `storeVec<T>` | `mvec[e][i]` |
| `$mat[r][c]` | `storeMat<T>` | `mat[e][r][c]` via `Mat<T>` |
| `$$n` | `param<int>` | `*(loop_counter)` |

Map chains (`$a->$b->$c`) are expanded to nested index operations.

## Option Handling

Rule options affect code generation:

| Option | Effect on generated code |
|--------|--------------------------|
| `option(disable_threading)` | Route to `compute(seq)` instead of `calculate(e)` |
| `option(no_dynamic_constraints)` | Suppress dynamic constraint checking in the generated sequence loop |

---

*See also:* [[source-language/lpp|lpp (application view)]],
[[runtime/rule-class-interface|Rule Class Interface]],
[[runtime/rule-registration|Rule Registration]]
