---
title: HDF5 I/O
category: Program Lifecycle
status: complete
attribution: llm
reviewed: false
---

# HDF5 I/O

Loci provides a set of parallel-aware HDF5 wrapper functions for writing and reading
container data to disk. These are the standard mechanism for output rules that produce
plot files and for checkpoint/restart workflows.

All calls use `MPI_COMM_WORLD` internally and are safe to issue from any MPI rank;
the library coordinates collective I/O automatically.

## File Lifecycle Functions

**`hid_t Loci::hdf5CreateFile(const char *name, unsigned flags, hid_t create_id, hid_t access_id, size_t file_size_estimate=0)`**

Creates a new HDF5 file (or truncates an existing one when `flags = H5F_ACC_TRUNC`).
Returns an HDF5 file identifier. The `create_id` and `access_id` arguments accept
`H5P_DEFAULT` for standard property lists. The optional `file_size_estimate` hint
pre-allocates space and can improve write performance for large files.

**`hid_t Loci::hdf5OpenFile(const char *name, unsigned flags, hid_t access_id)`**

Opens an existing HDF5 file. Use `H5F_ACC_RDONLY` for read-only access (restart) or
`H5F_ACC_RDWR` for read-write access. Returns an HDF5 file identifier.

**`herr_t Loci::hdf5CloseFile(hid_t file_id)`**

Closes an open HDF5 file and flushes any pending writes.

## Container I/O Functions

**`void Loci::writeContainer(hid_t file_id, string vname, storeRepP var)`**

Writes the contents of a Loci container to the open file under the dataset name
`vname`. `var` must be a `storeRepP` — the type-erased handle obtained by calling
`.Rep()` on any Loci container (see below).

**`void Loci::readContainer(hid_t file_id, string vname, storeRepP var, entitySet readSet)`**

Reads the dataset named `vname` from the open file into `var`, restricting the read
to the entities in `readSet`. Used in restart and checkpointing workflows.

## The `.Rep()` Pattern

Loci containers (`store`, `storeVec`, `Map`, etc.) expose a `.Rep()` method that
returns a `storeRepP` — a `shared_ptr` to the type-erased container representation.
`writeContainer` and `readContainer` accept `storeRepP` so that a single I/O
implementation handles all container types:

```cpp
Loci::writeContainer(file_id, "temperature", $temperature.Rep()) ;
Loci::readContainer(file_id, "motionState", container.Rep(), readSet) ;
```

## Canonical Write Pattern

HDF5 I/O must occur in a [[rule-system/prelude-block|prelude block]] because it
involves collective MPI operations that cannot be interleaved with the per-entity
kernel loop. The rule must carry `option(disable_threading)` to prevent Loci from
parallelising the prelude itself:

```cpp
$rule pointwise(OUTPUT <- cell2node(temperature), $n, plot_modulo),
  constraint(pos), conditional(doPlot), option(disable_threading),
  prelude {
    string filename = "output/temperature." + to_string(*$$n) + ".hdf5" ;
    hid_t file_id = Loci::hdf5CreateFile(filename.c_str(),
                                          H5F_ACC_TRUNC,
                                          H5P_DEFAULT, H5P_DEFAULT) ;
    Loci::writeContainer(file_id, "temperature",
                         $cell2node(temperature).Rep()) ;
    Loci::hdf5CloseFile(file_id) ;
  } ;
```

Key points:
- The `prelude` block has no matching `compute` block; the rule body is entirely in `prelude`.
- `$n` is the iteration counter; the file name embeds it to produce per-timestep output.
- `H5F_ACC_TRUNC` creates the file, overwriting any previous file with the same name.
- No per-entity loop is needed; `writeContainer` handles all entities collectively.

## Canonical Read Pattern

Reading follows the same prelude structure. A typical restart rule reads persisted
state back into a container for a given entity set:

```cpp
hid_t file_id = Loci::hdf5OpenFile(filename.c_str(),
                                    H5F_ACC_RDONLY, H5P_DEFAULT) ;
Loci::readContainer(file_id, "motionState", container.Rep(), readSet) ;
Loci::hdf5CloseFile(file_id) ;
```

## Parallel I/O Mode

By default, Loci performs HDF5 I/O using a single-process (rank-0) serial path.
For large process counts, **parallel HDF5 I/O** — where each rank reads and writes
concurrently to a shared file — can substantially improve throughput.

### Command-Line Flags

Pass `--pio` to enable parallel I/O for the entire run; `--nopio` forces serial mode.
These flags are consumed by `Loci::Init`:

```bash
mpirun -np 40 mysolver --pio case.vog
```

### Programmatic Control

`set_parallel_io(bool)` switches between modes at runtime. It must be called
collectively (every rank must call it) and must not be called while a file is open:

```cpp
Loci::set_parallel_io(true) ;
hid_t fid = Loci::hdf5OpenFile("restart.hdf5", H5F_ACC_RDONLY, H5P_DEFAULT) ;
Loci::readContainer(fid, "temperature", $temperature.Rep(), readSet) ;
Loci::hdf5CloseFile(fid) ;
Loci::set_parallel_io(false) ;
```

The `writeContainer` and `readContainer` functions automatically use whichever mode
is active; no change to call sites is required.

## `multiStore` I/O

`writeContainer` and `readContainer` handle `store`, `storeVec`, and `param`
containers. For **`multiStore`** containers, use the dedicated template functions:

```cpp
// Write
Loci::writeMultiStore(file_id, "face2node", face2node_ms,
                      write_set, facts) ;

// Read
Loci::readMultiStore(file_id, "face2node", face2node_ms,
                     read_set, facts) ;
```

The `facts` argument supplies distribution information needed for parallel I/O. For
serial contexts `facts` may be omitted (overloads without it exist).

---

*See also:* [[rule-system/prelude-block|Prelude Block]],
[[rule-system/output|OUTPUT]], [[program-lifecycle/fact-db|fact_db]],
[[program-lifecycle/init-finalize|Loci::Init / Loci::Finalize]]
