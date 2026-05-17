---
title: EntitySet
category: Core Data Model
status: normative
---

# EntitySet

An **EntitySet** is a finite, unordered collection of [[core-data-model/entity|Entity]]
identifiers with true set semantics: insertion order is not preserved and duplicates are
silently ignored. EntitySets are the primary indexing domain for containers and maps,
and the domain over which rules execute.

Internally an EntitySet is stored as an ordered collection of non-overlapping
`interval` values (an `intervalSet`) for compact representation and efficient set
operations.

## Construction

### From an interval

An `interval(a, b)` represents the contiguous range of entity labels
$[a, b]$ inclusive. It is the most common way to construct an EntitySet:

```cpp
interval onedigit = interval(0, 9) ;      // labels 0 through 9
entitySet A = onedigit ;                  // entitySet from interval
entitySet B = interval(14, 100) ;         // direct construction
```

### From an arbitrary collection

```cpp
int vals[] = {10, 15, 12, 1, 14, 16, 17} ;
entitySet vset = create_entitySet(vals, vals+7) ;
// vset = ([1,1][10,10][12,12][14,17])

std::vector<int> vec ;
// ... fill vec ...
entitySet from_vec = create_entitySet(vec.begin(), vec.end()) ;
```

### By adding individual entities

```cpp
entitySet B = interval(14, 100) ;
Entity e10 = Entity(10) ;
B += e10 ;   // B is now ([10,10][14,100])
```

## C++ Variables vs. Loci Facts

It is important to distinguish between:

- **C++ variables** — ordinary `entitySet` (or `constraint`, `param`, etc.) objects
  manipulated directly in application code. They are unknown to the Loci scheduler
  unless explicitly registered in the [[program-lifecycle/fact-db|fact database]].
- **Loci facts** (named variables) — containers registered with the fact database under
  a string name, accessible to rules by that name and visible to the scheduler.

For example, `entitySet A = interval(0, 9)` is a plain C++ variable. Only after
`facts.create_fact("A", A)` does it become a Loci variable that rules can depend on.

## Distinguished Constants

`EMPTY` and `UNIVERSE` are both **named Loci facts** pre-registered in the fact
database by the runtime, making them visible to the scheduler and referenceable by
name in rule signatures. However, they differ in their C++ availability:

- `Loci::EMPTY` is also a **named C++ variable** — the empty entitySet — and is used
  directly in imperative code.
- `UNIVERSE` has **no corresponding C++ variable**. In imperative code the universal
  set is expressed as `~EMPTY` (the complement of `Loci::EMPTY`), which is the
  idiomatic form:

```cpp
*viscous = ~EMPTY ;   // assign universal set to a constraint (imperative context)
```

| Name | Kind | Meaning |
|------|------|---------|
| `Loci::EMPTY` | Named Loci fact + C++ variable | The empty EntitySet |
| `UNIVERSE` | Named Loci fact only | The universal set; available in rule `constraint()` clauses |
| `~EMPTY` | C++ expression | Universal entitySet value; preferred in imperative code |
| `Loci::UNIVERSE_MIN` | C++ integer constant | Smallest valid entity label |
| `Loci::UNIVERSE_MAX` | C++ integer constant | Largest valid entity label |

## Set Operations

Operator forms produce new EntitySets and are the preferred style:

| Operation | Operator | Example |
|-----------|----------|---------|
| Union | `A + B` | `entitySet D = A + B ;` |
| Intersection | `A & B` | `entitySet C = A & B ;` |
| Difference | `A - B` | `entitySet G = A - C ;` |
| Complement | `~A` | `entitySet U = ~EMPTY ;` |

In-place method forms (which modify the receiver) are also available:

```cpp
G.Union(interval(13, 32)) ;      // G = G ∪ [13,32]
G.Intersection(interval(13,32)) ;
G.Complement() ;                 // G = ~G
```

### Shift operators

The `>>` and `<<` operators shift all entity labels in an EntitySet by a constant,
then intersect with the original set to keep only labels that have a valid neighbour.
This is the standard idiom for computing adjacent entity sets from a node list:

```cpp
entitySet nodes = interval(0, 10) ;
entitySet left_nodes  = (nodes >> 1) & nodes ; // nodes that have a left neighbour
entitySet right_nodes = (nodes << 1) & nodes ;
```

## Query Methods

```cpp
entitySet A = interval(0, 9) ;

bool member  = A.inSet(5) ;      // true — test membership by integer label
int  lo      = A.Min() ;         // 0
int  hi      = A.Max() ;         // 9
int  n       = A.size() ;        // 10
int  nivals  = A.num_intervals() ; // 1 (stored as one interval [0,9])
bool equal   = A.Equal(A & A) ;  // true
```

## Iteration

```cpp
entitySet A = interval(0, 9) ;
entitySet::const_iterator ei ;
for(ei = A.begin(); ei != A.end(); ++ei) {
    // *ei is the integer label of the current entity
}
```

## Comparison

`less_than()` and `greater_than()` provide a lexicographic total order over EntitySets,
which is useful when EntitySets are used as map keys:

```cpp
if (A.less_than(B)) { /* ... */ }
```

## Sequences

A **sequence** (`sequence` type) is the ordered analogue of an EntitySet: it is a list
of entity labels where insertion order is significant and duplicates are permitted.
Application code rarely constructs sequences directly; the scheduler generates them to
specify per-rule execution order. When ordered traversal is required (e.g., for
Gauss-Seidel iteration), the `sequence` type provides concatenation (`+`) and
`Reverse()`.

```cpp
sequence vseq = create_sequence(vals, vals+7) ;
sequence Aseq = A ;             // entitySet → sequence (sorted ascending)
sequence Cseq = Aseq + vseq ;   // concatenation
Cseq.Reverse() ;
```

## Formal Definition

$S \subseteq U$, $|S| < \infty$, where
$U = \{ i \in \mathbb{Z} \mid \texttt{UNIVERSE\_MIN} \le i \le \texttt{UNIVERSE\_MAX} \}$.

---

*See also:* [[core-data-model/entity|Entity]], [[core-data-model/relation|Relation]],
[[core-data-model/constraint|Constraint]]
