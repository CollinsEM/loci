---
title: OUTPUT
category: Rule System
status: complete
attribution: llm
reviewed: false
---

# OUTPUT

**`OUTPUT`** is a special output variable conventionally used for side-effect rules —
rules whose purpose is to produce observable effects (file I/O, stdout diagnostics,
plot file generation) rather than to contribute to the primary computation. `OUTPUT`
rules are scheduled normally: they execute whenever their declared inputs are satisfied
and any [[rule-system/conditional|conditional]] clause evaluates to true.

## Automatic Scheduling in Loops

Because `OUTPUT` is automatically requested within every active
[[rule-system/iterative-loop|iterative loop]], rules producing it will execute every
iteration unless explicitly gated by a conditional. This is the standard mechanism for
periodic I/O: a conditional param computed each iteration determines whether the output
operation is triggered.

## The `disable_threading` Option

`OUTPUT` rules that perform file I/O or other non-re-entrant operations should be
annotated with `option(disable_threading)` to prevent concurrent invocation and ensure
that all processes act on the rule synchronously.

## Example

```cpp
$rule singleton(OUTPUT <- L2Norm(qresidual), $$n),
      option(disable_threading) {
  if(Loci::MPI_rank == 0)
    cout << "iter " << $$n << ": "
         << $L2Norm(qresidual) << endl ;
}
```

Note: `$$n` (the iteration counter param) is accessed without `*` in the compute block.

---

*See also:* [[rule-system/conditional|Conditional]],
[[rule-system/iterative-loop|Iterative Loop]],
[[rule-system/prelude-block|Prelude Block]]
