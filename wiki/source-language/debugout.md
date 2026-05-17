---
title: "Loci::debugout"
category: Loci Source Language
status: complete
attribution: llm
reviewed: false
---

# Loci::debugout

**`Loci::debugout`** is an output stream, used analogously to `std::cerr`, that
directs diagnostic output to per-process debug files. A conforming runtime creates
these files automatically in a `debug/` subdirectory of the working directory. Each
parallel process writes to its own debug file, making it possible to inspect per-process
state without interleaving output from multiple processes on the terminal.

`Loci::debugout` is a development utility intended for use during solver development
and debugging. It has no effect on scheduling or execution semantics.

## Example

```cpp
$[Once] {
  Loci::debugout << "rank 0: temperature = " << $temperature << endl ;
}
```

---

*See also:* [[source-language/dollar-once|$[Once]]]
