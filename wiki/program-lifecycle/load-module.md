---
title: "Loci::load_module"
category: Program Lifecycle
status: complete
attribution: llm
reviewed: false
---

# Loci::load_module

**`Loci::load_module`** loads a named Loci module — a shared library containing a set
of rules compiled independently of the main executable — and adds its rules to a
provided [[program-lifecycle/rule-db|rule_db]]. It is the normative interface for
dynamic rule loading.

```cpp
Loci::load_module("fvm", rdb) ;
```

In addition to loading the shared library and registering its rules, `load_module`
performs implementation-defined housekeeping operations required for correct module
integration. The behavioural guarantee is that after `load_module` returns, all rules
provided by the named module are available in `rdb` for schedule construction.

## The `fvm` Module

The `fvm` module is the standard finite-volume module provided with the Loci
distribution. It supplies rules for grid metrics, spatial gradients, face
extrapolations, nodal interpolations, and linear system solvers. Its services are
described in the [[fvm/index|FVM Module]] section of this reference.

---

*See also:* [[program-lifecycle/rule-db|rule_db]],
[[program-lifecycle/global-rule-list|global_rule_list]]
