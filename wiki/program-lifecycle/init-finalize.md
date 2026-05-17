---
title: "Loci::Init / Loci::Finalize"
category: Program Lifecycle
status: normative
---

# Loci::Init / Loci::Finalize

`Loci::Init` and `Loci::Finalize` bracket the lifetime of the Loci runtime. No Loci
functionality may be used before `Loci::Init` is called or after `Loci::Finalize` is
called.

```cpp
int main(int argc, char *argv[]) {
  Loci::Init(&argc, &argv) ;
  // ... Loci program ...
  Loci::Finalize() ;
  return 0 ;
}
```

## Loci::Init Behavioural Guarantees

- Initialises MPI (`MPI_Init`). A Loci application must **not** call `MPI_Init` directly.
- If Loci was built with PETSc support, initialises the PETSc library (`PetscInitialize`).
- Parses `argc`/`argv` for Loci-specific command-line flags (e.g., `--scheduleoutput`,
  `--nochomp`, `--debug`) and removes all recognised flags — including those recognised
  by MPI and PETSc — from the argument list. After `Loci::Init` returns, `argc` and
  `argv` contain only arguments not recognised by Loci or any library it initialises.
- Sets up Loci internal state required by the scheduler, fact database, and parallel
  communication infrastructure.

> **Important:** the set of flags consumed by `Loci::Init` is
> build-configuration-dependent. Application code must not assume which specific flags
> will or will not be present in `argv` after the call returns.

## Loci::Finalize Behavioural Guarantees

- Releases all Loci internal state.
- Finalises PETSc (if initialised) and MPI. A Loci application must **not** call
  `MPI_Finalize` directly.

## Loci::Abort

**`Loci::Abort()`** performs a clean collective abort across all MPI processes. It is
the correct way to terminate a Loci application on an unrecoverable error — preferable
to calling `MPI_Abort` or `exit` directly, as it allows Loci and MPI to perform
cleanup:

```cpp
if(!Loci::makeQuery(rdb, facts, "solution")) {
  cerr << "query failed!" << endl ;
  Loci::Abort() ;
}
```

`Loci::Abort()` does not return. It may be called from any MPI rank; the call is
collective and all processes terminate.

## Loci::version

**`Loci::version()`** returns a `string` identifying the version of the Loci library
in use. Useful for diagnostics and build verification:

```cpp
cout << "Loci version: " << Loci::version() << endl ;
```

---

*See also:* [[program-lifecycle/rule-db|rule_db]], [[program-lifecycle/fact-db|fact_db]],
[[program-lifecycle/make-query|Loci::makeQuery]]
