---
title: multiMap
category: Core Data Model
status: complete
attribution: llm
reviewed: false
---

# multiMap

A **multiMap** is a [[core-data-model/relation|Relation]] whose codomain is a
variable-length sequence of [[core-data-model/entity|Entity]] identifiers. multiMaps
encode one-to-many structural relationships (e.g., from a face to all of its bounding
nodes; from a cell to all of its faces).

## Kernel Access Syntax

Elements are accessed via integer indexing: `$multiMapName[i]->relation` accesses the
relation on the i-th entity in the sequence for the current execution entity. The
sequence length for entity `e` is accessed via `$multiMapName.num_elems(e)`.

## Formal Definition

$M : D \to U^*$, where $U^*$ denotes a finite sequence of entity identifiers of
variable length.

## Example

`face2node` maps each face to its ordered list of bounding nodes. The position of the
k-th node of the current face is accessed as `$face2node[k]->$pos` within a rule
executing over faces.

---

*See also:* [[core-data-model/map|Map]], [[core-data-model/map-vec|MapVec]]
