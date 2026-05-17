---
title: FVM Nodal Interpolation
category: FVM Module
status: complete
attribution: llm
reviewed: false
---

# FVM Nodal Interpolation

The `fvm` module provides parametric rules that interpolate cell-centred
(and boundary-face) quantities to mesh nodes. Nodal values are used primarily
for output (HDF5 plot files, `extract` post-processing) where visualisation
tools require node-centred data.

All `cell2node` variants produce **single-precision** (`float`) results by
design — this is intentional to reduce output file size for visualisation.

## Types

| Type | Container | Meaning |
|---|---|---|
| `cell2node(X)` | `store<float>` | Scalar `X` interpolated to nodes |
| `cell2node_v(X)` | `storeVec<float>` | General vector `X` interpolated to nodes |
| `cell2node_v3d(X)` | `store<vector3d<float>>` | 3-D vector `X` interpolated to nodes |
| `cell2nodeMax(X)` | `store<float>` | Maximum of neighbouring cell values at each node |
| `cell2nodeMin(X)` | `store<float>` | Minimum of neighbouring cell values at each node |
| `cell2nodeMaxMag(X)` | `store<float>` | Maximum magnitude of neighbouring cell scalars |
| `cell2nodeMaxv3d(X)` | `store<vector3d<float>>` | Per-component maximum of neighbouring cell vectors |

## Inputs Required

`cell2node(X)` draws from both `geom_cells` (interior) and boundary faces
(where `ci` maps each boundary face to its adjacent cell). To interpolate
a variable `X`, both `X` on `geom_cells` and `X_f` on boundary faces must
be available. In a heat solver this means the same `temperature` and
`temperature_f` rules that drive the gradient computation also feed the
nodal interpolation.

## Typical Use — Writing a Plot File

```cpp
$type doPlot param<bool> ;

$rule singleton(doPlot <- $n, plot_freq) {
  $doPlot = ((*$$n % $plot_freq) == 0) ;
}

$rule pointwise(OUTPUT <- cell2node(temperature), $n, plot_modulo),
  constraint(pos), conditional(doPlot), option(disable_threading),
  prelude {
    ostringstream oss ;
    oss << "output/temperature_hdf5." << (*$$n % *$plot_modulo) ;
    string filename = oss.str() ;
    if(Loci::MPI_rank == 0)
      cout << "writing " << filename << endl ;
    hid_t file_id = Loci::hdf5CreateFile(filename.c_str(),
                                          H5F_ACC_TRUNC,
                                          H5P_DEFAULT, H5P_DEFAULT) ;
    Loci::writeContainer(file_id, "temperature",
                         $cell2node(temperature).Rep()) ;
    Loci::hdf5CloseFile(file_id) ;
  } ;
```

The rule is constrained to `pos` (nodes) because `cell2node` values live on
nodes. `option(disable_threading)` is required because `hdf5CreateFile` and
`writeContainer` are collective MPI calls.

---

*See also:* [[fvm/gradients|Spatial Gradients]],
[[program-lifecycle/hdf5-io|HDF5 I/O]],
[[rule-system/output|OUTPUT]]
