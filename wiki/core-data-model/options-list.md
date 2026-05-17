---
title: options_list
category: Core Data Model
status: complete
attribution: llm
reviewed: false
---

# options_list

**`Loci::options_list`** is a key-value parameter container used to pass structured
configuration data through Loci containers. It is the value type behind
`param<options_list>` (application-level configuration) and `store<options_list>`
(per-entity configuration such as `BC_options` in the FVM module). It is exposed in
application code via `<Loci.h>`.

## .vars File Syntax

An `options_list` value is written in a `.vars` file as an angle-bracket-delimited,
comma-separated list of `key=value` pairs:

```
boundary_conditions: < BC_1=adiabatic, BC_2=specified(Twall=300K) >
initialConditions:   < T=300K, p=1atm, M=0.3 >
solver_options:      < tolerance=1e-8, max_iters=200 >
```

Values may be:
- bare names (`adiabatic`)
- numeric values (`1e-8`)
- numeric values with physical unit suffixes (`300K`, `1atm`, `0.3`)
- function-call style with sub-options (`specified(Twall=300K)`)
- quoted strings (`"output_dir"`)
- boolean values (`true`, `false`)

## Querying the Value Type

Before extracting a value, call `getOptionValueType` to identify what kind of
value a key holds:

| `option_value_type` | Meaning |
|---|---|
| `REAL` | Plain numeric value |
| `UNIT_VALUE` | Numeric value with physical unit |
| `NAME` | Bare identifier string |
| `FUNCTION` | Identifier followed by a sub-options list |
| `STRING` | Quoted string |
| `BOOLEAN` | `true` or `false` |
| `LIST` | Comma-separated list of sub-values |
| `NOT_ASSIGNED` | Key absent |

```cpp
options_list::option_value_type vt = $BC_options.getOptionValueType("Twall") ;
if(vt == Loci::UNIT_VALUE) {
  // extract with unit conversion
}
```

## Reading Values

### `getOption` — unit-free extraction

```cpp
double tol ;
$opts.getOption("tolerance", tol) ;    // extract as double

std::string name ;
$opts.getOption("scheme", name) ;      // extract NAME or STRING as std::string

bool flag ;
$opts.getOption("verbose", flag) ;     // extract BOOLEAN
```

### `getOptionUnits` — value with unit conversion

The runtime converts the stored value to the requested unit before returning it.

```cpp
double Twall ;
$BC_options.getOptionUnits("Twall", "kelvin", Twall) ;  // result in kelvin

double pressure ;
$BC_options.getOptionUnits("p", "Pa", pressure) ;        // converts from any unit to Pa
```

`getOptionUnits` also supports `vect3d` output for 3-component options.

### `checkOption` — named value test

Returns `true` if the key has type `NAME` and that name matches the given string.
Used to test which model or condition is selected:

```cpp
if($BC_options.checkOption("bc_type", "adiabatic")) { ... }
```

### `optionExists` — key presence test

```cpp
if($BC_options.optionExists("Twall")) {
  // Twall was specified for this boundary
}
```

### `getOptionNameList` — iterate over all keys

```cpp
auto names = $opts.getOptionNameList() ;
for(auto &key : names)
  cerr << "key: " << key << endl ;
```

## Setting Values (Imperative Use)

`setOption` inserts or overwrites a key. Used when constructing an `options_list`
programmatically (e.g., to build an `initialConditions` fact from defaults):

```cpp
options_list ol ;
ol.setOption("T",    300.0) ;
ol.setOption("scheme", std::string("implicit")) ;
```

## Example: Boundary Condition Rule

```cpp
// Extract wall temperature from BC_options for faces with a Twall specification
$rule pointwise(Twall <- BC_options),
      constraint(Twall_BCoption) {
  $BC_options.getOptionUnits("Twall", "kelvin", $Twall) ;
}
```

```cpp
// Select BC behaviour based on a named option
$rule pointwise(flux <- BC_options, temperature_f, area),
      constraint(convective_BC) {
  if($BC_options.checkOption("model", "Newton_cooling")) {
    double h ;
    $BC_options.getOptionUnits("h", "W/m^2/K", h) ;
    $flux = h * $area.sada * $temperature_f ;
  } else {
    $flux = 0.0 ;
  }
}
```

---

*See also:* [[program-lifecycle/vars-file|.vars File Format]],
[[fvm/mesh-topology|FVM Mesh Topology]],
[[core-data-model/param|param]],
[[core-data-model/store|store]],
[[core-data-model/data-schema-traits|data_schema_traits]]
