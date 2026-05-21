---
title: Data-Driven Computation Principle
category: Foundational Principles
status: complete
audience: both
attribution: human
reviewed: false
---

# Data-Driven Computation

Loci is based on a data driven computation paradigm. This is paradigm
maps directly onto the typical problem solving approach of most
scientists and engineers:

<!-- 1. Start with a set of [[program-lifecycle/fact-db|facts]] that are -->
<!--    already known or assumed to be true, and a -->
<!--    [[program-lifecycle/make-query|query]] about some aspect of the -->
<!--    system that needs to be derived. -->
1. Start with a set of **facts** that are already known or assumed to
   be true, and a **query** about some aspect of the system that needs
   to be derived.
<!-- 2. Determine the domain over which a solution is to be obtained, and -->
<!--    discretize the domain if necessary and establish the -->
<!--    [[fvm/mesh-topology|topological relationships]] of the discrete -->
<!--    entities. -->
2. Determine the domain over which a solution is to be obtained, and
   discretize the domain if necessary and establish the topological
   relationships of the discrete entities.
3. Assign realistic initial values to the quantities of interest on
   these discrete entities.
<!-- 4. Compile a set of [[rule-system/rule|rules]] for transforming -->
<!--    known quantities into unknown quantities based on established -->
<!--    physical laws and/or numerical algorithms. -->
4. Compile a set of **rules** for transforming known quantities into
   unknown quantities based on established physical laws and/or
   numerical algorithms.
<!-- 5. Use these rules and the topological relationships over the domain -->
<!--    to establish a [[scheduling/dependency-graph|graph]] of -->
<!--    dependent computations. -->
5. Use these rules and the topological relationships over the domain
   to establish a graph of dependent computations.
6. Given the query from the user for a particular value or set of
   values, create a schedule of calculations that will generate the
   requested information from the provided facts based on the initial
   assumptions.
7. Execute the computations in the most efficient manner possible over
   the provided computational units.
   
# Implementation

Rules are a logical abstraction of a transformation from one set of
known values into another value that is not yet known. It is at this
level of granularity that the Loci scheduler works.

The ability of Loci to schedule a rule for computation is driven
entirely by the availability of the input values that it depends
upon. 

The availability is determined by the existence of entities that
possess attributes corresponding to the required values, and the
topological relationships that connect entities accross the solution
manifold (e.g. the computational domain).

<!-- A rule becomes eligible to execute when — and only when — all of its -->
<!-- declared inputs exist in the  -->
<!-- [[program-lifecycle/fact-db|fact database]] -->
<!-- over the required entity domains. -->

A rule becomes eligible to execute when — and only when — all of its
declared inputs exist in the **fact database** over the
required entity domains.

The Loci application developer does not explicitly control when and
how a rule will execute. They merely specify the logical dependencies
of the data required for accurate computation.

<!-- The responsibility for correctly and efficiently carrying out these -->
<!-- computations (in parallel if possible) is delegated entirely to the -->
<!-- [[scheduling/scheduler|Loci runtime scheduler]]. -->

The responsibility for correctly and efficiently carrying out these
computations (in parallel if possible) is delegated entirely to the
**Loci runtime scheduler**.

## Implications

- The programmer declares what is needed for a computation, not when
  to compute it.
- The scheduler determines the execution order and distributes the
  required data and computational kernels to available processing
  units.
- A full schedule can be requested by providing the `--scheduleoutput`
  option on the command line. The `schedule` file will be output in
  the `debug` subdirectory.
- A rule with unsatisfied inputs is pruned from the computational
  graph.
- If a rule is pruned, a diagnostic message will be left in a `debug`
  file located within the `debug` subdirectory.
- This pruning behavior is often used to control conditional execution
  of specific solver functionality through the use of **optional rules**.
  <!-- [[rule-system/optional-rule|optional rules]]. -->

---

*See also:* 
Scheduler,
Dependency Graph,
Optional Rule,
Debugging,
Fact Database,
Rule Database,
Make Query,
Mesh Topology]

<!-- [[scheduling/scheduler|Scheduler]], -->
<!-- [[scheduling/dependency-graph|Dependency Graph]], -->
<!-- [[rule-system/optional-rule|Optional Rule]], -->
<!-- [[program-lifecycle/debugging|Debugging]], -->
<!-- [[program-lifecycle/fact-db|Fact Database]] -->
<!-- [[program-lifecycle/rule-db|Rule Database]] -->
<!-- [[program-lifecycle/make-query|Make Query]], -->
<!-- [[fvm/mesh-topology|Mesh Topology]] -->
