---
title: Halo Exchange
category: Distributed Execution
status: normative
audience: both
---

# Halo Exchange

A **halo exchange** is a runtime communication operation in which Relation values for
[[distributed-execution/ghost-entity|ghost entities]] are updated from their owning
processes to their neighbouring processes. Halo exchanges are inserted automatically
by the [[scheduling/scheduler|scheduler]] wherever a rule's map-chain dependencies
cross process boundaries, and are entirely transparent to the application developer.

---

*See also:* [[distributed-execution/ghost-entity|Ghost Entity]],
[[scheduling/scheduler|Scheduler]]
