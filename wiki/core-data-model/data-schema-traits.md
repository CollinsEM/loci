---
title: data_schema_traits
category: Core Data Model
status: complete
attribution: llm
reviewed: false
---

# data_schema_traits

**`data_schema_traits`** is the normative interface by which a user-defined value type
`T` registers its serialisation behaviour with the Loci runtime. Any type `T` used as
the value type of a Loci container (`store<T>`, `param<T>`, `storeVec<T>`,
`blackbox<T>`, etc.) must have a specialisation of this template so that the runtime
can serialise and deserialise values of that type for inter-process communication and
portable file I/O.

## Two Forms of Specialisation

### Identity Schema (`IDENTITY_CONVERTER`)

Used when `T` occupies a contiguous, fixed-size region of memory with a layout
compatible with direct bitwise copy — appropriate for plain structs containing only
atomic or fixed-size array members. The specialisation must provide a static
`get_type()` method returning a `DatatypeP` describing the memory layout.

```cpp
namespace Loci {
  template <> struct data_schema_traits<MyStruct> {
    typedef IDENTITY_CONVERTER Schema_Converter;
    static DatatypeP get_type() {
      CompoundDatatypeP c = CompoundFactory(MyStruct());
      LOCI_INSERT_TYPE(c, MyStruct, member1);
      LOCI_INSERT_TYPE(c, MyStruct, member2);
      return DatatypeP(c);
    }
  };
}
```

### User-Defined Schema (`USER_DEFINED_CONVERTER`)

Used when `T` contains heap-allocated or variable-size members (e.g., STL containers,
pointers). The specialisation must name a converter class implementing:

| Method | Purpose |
|--------|---------|
| `int getSize() const` | Returns the number of atomic elements needed to represent the object |
| `void getState(base_type *buf, int &size)` | Serialises the object into a contiguous buffer |
| `void setState(base_type *buf, int size)` | Reconstructs the object from a contiguous buffer |

## Built-in Types

The built-in Loci types (`vector3d<T>`, `vector2d<T>`, `tensor3d<T>`, `Array<T,N>`,
and all standard C++ atomic types) have pre-registered `data_schema_traits`
specialisations provided by the implementation. Application developers do not need to
supply them.

---

*See also:* [[core-data-model/relation|Relation]], [[core-data-model/store|store]],
[[core-data-model/param|param]]
