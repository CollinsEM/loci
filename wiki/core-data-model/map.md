---
title: Map
category: Core Data Model
status: complete
attribution: llm
reviewed: false
---

# Map

A **Map** is a [[core-data-model/relation|Relation]] whose codomain is a single
[[core-data-model/entity|Entity]] identifier. Maps encode one-to-one or many-to-one
structural (topological) relationships between entities.

## Kernel Access Syntax

Maps are used in rule kernels via the `map->relation` composition syntax, which
navigates from a source entity to an adjacent entity and accesses a relation on that
entity. Multiple maps may be chained (e.g., `cell2face->face2node->pos`). This syntax
is valid for both reading inputs and writing outputs within a rule kernel.

## Formal Definition

$M : D \to U$.

## Example

`cl: {faces} → {cells}` maps each face to its left-adjacent cell; `cr` maps each
face to its right-adjacent cell. Within a rule executing over faces, `$cl->$pressure`
accesses the pressure of the left cell.

---

*See also:* [[core-data-model/multi-map|multiMap]], [[core-data-model/map-vec|MapVec]],
[[core-data-model/relation|Relation]]
