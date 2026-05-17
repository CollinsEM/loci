---
title: generalize
category: Scheduling and Execution Model
status: normative
audience: both
---

# generalize

**Generalize** is a scheduler-internal operation, inserted automatically into the
execution schedule, that unifies the output of a [[rule-system/build-rule|build rule]]
(`u{n=0}`) with the loop variable (`u{n}`) for the first iteration of an
[[rule-system/iterative-loop|iterative loop]]. After the first iteration, `u{n}` is
set to the value computed for `u{n+1}` by the preceding
[[rule-system/advance-rule|advance rule]].

## Transparency

Generalize is transparent to the application developer and is documented here for
reference when reading scheduler output. The precise rules governing generalize
belong to the Loci Runtime Specification.

---

*See also:* [[scheduling/promote|promote]], [[rule-system/build-rule|Build Rule]],
[[rule-system/iterative-loop|Iterative Loop]]
