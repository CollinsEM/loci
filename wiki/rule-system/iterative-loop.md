---
title: Iterative Loop
category: Rule System
status: normative
---

# Iterative Loop

An **iterative loop** is a structured repetition construct in the Loci execution model,
recognised and generated automatically by the [[scheduling/scheduler|scheduler]] from
the [[rule-system/build-rule|build]] / [[rule-system/advance-rule|advance]] /
[[rule-system/collapse-rule|collapse]] rule pattern. The loop repeats until the
[[rule-system/conditional|conditional]] variable associated with the collapse rule
evaluates to true.

## The Iteration Index `$$n`

The current iteration number is available within all rules executing inside the loop
via the special integer param `$$n`. This variable is managed automatically by the
scheduler and advances by one each time the advance rules complete. It is accessed as
`$$n` in the compute block (no `*` required).

## Generality

The iterative loop is not limited to physical time-stepping. It applies equally to:

- Pseudo-time iterations
- Newton solves
- Runge-Kutta stages
- Any fixed-point or multi-step iterative algorithm

Nested loops are supported, enabling, for example, an inner Newton iteration within
an outer time-stepping loop.

## Nested Loops

Loops may be nested to arbitrary depth. A common pattern is an inner Newton or
linear-solver iteration inside an outer time-stepping loop. Loci uses a **time-level
annotation** to distinguish variables at each nesting level. The outermost loop uses
`{n}`, an inner loop adds a second index `{n,it}`, a third level adds `{n,it,igs}`,
and so on.

```
Outer loop (time-stepping):   Q{n},  Q{n+1}
Inner loop (Newton):          Q{n,it}, Q{n,it+1}
```

The inner build rule initialises the Newton variable from the outer time-level value:

```
build rule (inner):   Q{n,it=0} ← Q{n}
advance rule (inner): Q{n,it+1} ← Q{n,it}, R{n,it}
collapse rule (inner): Q{n+1}   ← Q{n,it},
                        conditional(converged{n,it})
```

From the outer loop's perspective, `Q{n+1}` is just a derived fact — the inner
iteration is a black box whose structure is determined by the scheduler.

Application code does not write time-level annotations directly. The annotation
(`{n}`, `{n,it}`, etc.) is inferred by the scheduler from the nesting structure of
the build/advance/collapse rule sets present in the rule database.

## Promote and Generalise

The scheduler automatically inserts [[scheduling/promote|promote]] operations to make
stationary variables available inside the loop and [[scheduling/generalize|generalize]]
operations to unify the build-rule output with the loop variable for the first
iteration. These are transparent to the application developer.

## Loop Structure Summary

```
build rule:    Q{n=0} ← initial conditions          (fires once, before loop)
advance rule:  Q{n+1} ← Q{n}, dt{n}, R{n}          (fires each iteration)
collapse rule: solution ← Q{n},                     (fires when done)
               conditional(finishTimestep{n})
```

---

*See also:* [[rule-system/build-rule|Build Rule]], [[rule-system/advance-rule|Advance Rule]],
[[rule-system/collapse-rule|Collapse Rule]], [[rule-system/conditional|Conditional]],
[[scheduling/promote|promote]], [[scheduling/scheduler|Scheduler]]
