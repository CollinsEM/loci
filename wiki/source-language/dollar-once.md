---
title: $[Once]
category: Loci Source Language
status: complete
attribution: llm
reviewed: false
---

# $[Once]

The **`$[Once]`** construct wraps a block of code that should execute on *exactly one
process* in a parallel run. It is used inside rule kernels to ensure that diagnostic
messages, error reports, or other process-global output are emitted exactly once rather
than once per MPI rank or thread.

## Syntax

```cpp
$rule singleton(Density <- materialProperties) {
  if(!$materialProperties.optionExists("density")) {
    $[Once] {
      cerr << "ERROR: density not defined in materialProperties" << endl ;
    }
    Loci::Abort() ;
  }
}
```

## Behavioural Guarantee

A conforming runtime must ensure that the body of a `$[Once]` block executes on exactly
one process, regardless of the parallel execution configuration. Which process executes
the block is an implementation choice; the guarantee is uniqueness of execution, not
identity of the executing process.

## Scope

`$[Once]` is appropriate both for internal error messages during solver development and
for user-facing terminal output that should appear once (e.g., printing a configuration
summary at startup).

---

*See also:* [[source-language/dollar-rule|$rule syntax]],
[[source-language/debugout|Loci::debugout]]
