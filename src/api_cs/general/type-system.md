# Type System Reflection

REFramework.NET exposes the RE Engine's type database through three core reflection classes: `TypeDefinition`, `Method`, and `Field`. These let you inspect and interact with any type at runtime — look up methods, read fields, create instances, and invoke functions dynamically.

## TypeDefinition

Represents a type in the game's type database (TDB). Every class, struct, enum, and primitive in the engine has a corresponding `TypeDefinition`.

### Getting a TypeDefinition

```csharp
// By name
var tdb = API.GetTDB();
var typeDef = tdb.FindType("app.SaveManager");

// From a ManagedObject
var mo = ManagedObject.ToManagedObject(address);
var typeDef = mo.GetTypeDefinition();
```

### Identity

| Property       | Type     | Description                                   |
|----------------|----------|-----------------------------------------------|
| `Name`         | `string` | Short type name (e.g. `"SaveManager"`)        |
| `Namespace`    | `string` | Namespace (e.g. `"app"`)                      |
| `FullName`     | `string` | Fully qualified name (e.g. `"app.SaveManager"`) |
| `Index`        | `uint`   | Global index in the type database             |
| `Size`         | `uint`   | Instance size in bytes                        |
| `ValueTypeSize`| `uint`   | Size when used as a value type                |

### Type Queries

```csharp
bool isVal    = typeDef.IsValueType();
bool isEnum   = typeDef.IsEnum();
bool isByRef  = typeDef.IsByRef();
bool isPtr    = typeDef.IsPointer();
bool isPrim   = typeDef.IsPrimitive();
bool isGeneric = typeDef.IsGenericType();
```

`GetVMObjType()` returns a `VMObjType` enum describing the runtime category:

| Value | Name       | Meaning              |
|-------|------------|----------------------|
| 0     | `NULL_`    | Null/invalid         |
| 1     | `Object`   | Reference type       |
| 2     | `Array`    | Array                |
| 3     | `String`   | System.String        |
| 4     | `Delegate` | Delegate             |
| 5     | `ValType`  | Value type           |

### Type Hierarchy

| Property / Method                      | Returns            | Description                              |
|----------------------------------------|--------------------|------------------------------------------|
| `ParentType`                           | `TypeDefinition`   | Direct base type                         |
| `DeclaringType`                        | `TypeDefinition`   | Enclosing type (for nested types)        |
| `UnderlyingType`                       | `TypeDefinition`   | Underlying integer type (enums only)     |
| `ElementType`                          | `TypeDefinition`   | Element type (arrays only)               |
| `IsDerivedFrom(string name)`           | `bool`             | Inheritance check by name                |
| `IsDerivedFrom(TypeDefinition other)`  | `bool`             | Inheritance check by TypeDefinition      |
| `GetGenericArguments()`                | list               | Generic type parameters                  |

```csharp
if (typeDef.IsDerivedFrom("app.EnemyCharacter")) {
    API.LogInfo($"{typeDef.FullName} is an enemy");
}
```

### Member Lookup

```csharp
// Single member by name
Method method = typeDef.GetMethod("doSomething");
Method method = typeDef.FindMethod("doSomething"); // alias
Field  field  = typeDef.GetField("_Health");
Field  field  = typeDef.FindField("_Health");       // alias

// All members
var methods = typeDef.GetMethods(); // or typeDef.Methods
var fields  = typeDef.GetFields();  // or typeDef.Fields
```

### Creating Instances

```csharp
// Create a new managed object instance (NOT globalized — you must globalize if keeping a reference)
ManagedObject instance = typeDef.CreateInstance(0);

// Create a boxed value type
ValueType vt = typeDef.CreateValueType();

// Create a managed array of this element type (NOT globalized)
ManagedObject array = typeDef.CreateManagedArray(10); // 10 elements
```

> **Important:** `CreateInstance` and `CreateManagedArray` return non-globalized objects. If you store a reference beyond the current frame, call `.Globalize()` to prevent the GC from collecting it.

### Static Fields

The `Statics` property returns a `NativeObject` that provides access to static fields on the type:

```csharp
var statics = typeDef.Statics;
var val = (statics as IObject).GetField("_SomeStaticField");
```

### Runtime Reflection

| Property / Method      | Returns               | Description                                      |
|------------------------|-----------------------|--------------------------------------------------|
| `RuntimeType`          | `ManagedObject`       | The `System.Type` instance for this type         |
| `GetRuntimeMethods()`  | `List<ManagedObject>` | `System.MethodInfo` objects for runtime reflection |

---

## Method

Represents a method in the type database.

### Identity

| Property / Method  | Returns          | Description                                      |
|--------------------|------------------|--------------------------------------------------|
| `Name`             | `string`         | Method name                                      |
| `Index`            | `uint`           | Global index in the TDB                          |
| `VirtualIndex`     | `int`            | Virtual table index (`-1` if non-virtual)        |
| `DeclaringType`    | `TypeDefinition` | Type that declares this method                   |
| `ReturnType`       | `TypeDefinition` | Return type                                      |
| `IsStatic()`       | `bool`           | Static method check                              |
| `IsVirtual()`      | `bool`           | Virtual method check                             |
| `IsOverride()`     | `bool`           | Override check                                   |
| `GetFunctionPtr()` | `IntPtr`         | Raw native function pointer (advanced interop)   |

### Parameters

```csharp
uint count = method.GetNumParams();
var  parameters = method.GetParameters(); // or method.Parameters

foreach (var param in parameters) {
    API.LogInfo($"  {param.Name}: {param.Type.FullName}");
}
```

Each `MethodParameter` has `Name` (string) and `Type` (TypeDefinition).

### Invocation

**`InvokeBoxed`** is the easiest way to call a method — it auto-converts the return value:

```csharp
var method = typeDef.GetMethod("getHealth");
int hp = (int)method.InvokeBoxed(typeof(int), instance, new object[] { });
```

```csharp
// With arguments
var setter = typeDef.GetMethod("setDamageMultiplier");
setter.InvokeBoxed(typeof(void), instance, new object[] { 2.5f });
```

**`Invoke`** returns the raw `InvokeRet` struct (see below) for cases where you need low-level control:

```csharp
InvokeRet ret = method.Invoke(instance, new object[] { 42 });
if (!ret.ExceptionThrown) {
    int result = (int)ret.DWord;
}
```

**`HandleInvokeMember_Internal`** is used internally for dynamic dispatch:

```csharp
object result = null;
bool ok = method.HandleInvokeMember_Internal(instance, new object[] { 42 }, ref result);
```

### Dynamic Hooking

`AddHook` creates a runtime hook on a method — an alternative to the attribute-based `[MethodHook]` approach. Useful when you need to hook methods discovered dynamically.

```csharp
var method = typeDef.GetMethod("update");
var hook = method.AddHook(false); // ignoreJmp = false

hook.AddPre(args => {
    API.LogInfo("update() called!");
    return PreHookResult.Continue;
});

hook.AddPost(args => {
    API.LogInfo("update() returned");
});
```

The `ignoreJmp` parameter controls whether the hook should ignore JMP trampolines at the function entry. Set to `false` unless you have a specific reason.

---

## Field

Represents a field in the type database.

### Identity

| Property / Method | Returns          | Description                                    |
|-------------------|------------------|------------------------------------------------|
| `Name`            | `string`         | Field name                                     |
| `Index`           | `uint`           | Global index in the TDB                        |
| `Flags`           | `uint`           | Raw field flags                                |
| `DeclaringType`   | `TypeDefinition` | Type that declares this field                  |
| `Type`            | `TypeDefinition` | The field's type                               |
| `IsStatic()`      | `bool`           | Static field check                             |
| `IsLiteral()`     | `bool`           | Compile-time constant (`const`) check          |
| `OffsetFromBase`  | `uint`           | Byte offset from the object base address       |

### Data Access

```csharp
var field = typeDef.GetField("_Health");
ulong objAddress = /* ... */;

// Read — auto-boxed to a C# object
object value = field.GetDataBoxed(objAddress, false);

// Write
field.SetDataBoxed(objAddress, 999, false);

// Raw pointer access (advanced)
IntPtr raw = field.GetDataRaw(objAddress, false);
```

> **GOTCHA: The `isValueType` parameter**
>
> The `isValueType` parameter on `GetDataRaw`, `GetDataBoxed`, and `SetDataBoxed` refers to whether the **containing object** is a value type — **NOT** whether the field itself is a value type.
>
> Getting this wrong silently reads from or writes to the wrong memory offset.
>
> ```csharp
> // Object is a ManagedObject (reference type) — isValueType = false
> field.GetDataBoxed(managedObjAddr, false);
>
> // Object is a ValueType — isValueType = true
> field.GetDataBoxed(valueTypeAddr, true);
> ```
>
> When in doubt: if you got the object from `ManagedObject.ToManagedObject()`, pass `false`. If you got it from `TypeDefinition.CreateValueType()` or it lives inside a struct, pass `true`.

---

## InvokeRet

`InvokeRet` is a 128-byte explicit-layout union struct returned by `Method.Invoke()`. All value fields overlap at offset 0, so you read whichever field matches the method's return type.

### Fields

| Field      | Type     | Offset | Use for                       |
|------------|----------|--------|-------------------------------|
| `Byte`     | `byte`   | 0      | `System.Byte` returns         |
| `Word`     | `ushort` | 0      | `System.UInt16` returns       |
| `DWord`    | `uint`   | 0      | `System.UInt32` / `int` returns |
| `QWord`    | `ulong`  | 0      | `System.UInt64` / pointers    |
| `Float`    | `float`  | 0      | `System.Single` returns       |
| `Double`   | `double` | 0      | `System.Double` returns       |
| `Ptr`      | `IntPtr` | 0      | Raw pointer returns           |

| Field              | Type   | Offset | Description                  |
|--------------------|--------|--------|------------------------------|
| `ExceptionThrown`  | `bool` | 128    | `true` if the call threw     |

### Usage

Always check `ExceptionThrown` before reading the return value:

```csharp
var ret = method.Invoke(instance, new object[] { });

if (ret.ExceptionThrown) {
    API.LogError("Method threw an exception");
    return;
}

// Read the appropriate field for the return type
float health = ret.Float;
```

> **Prefer `InvokeBoxed`** for most use cases. `InvokeRet` is only needed when you want to avoid boxing overhead or need to interpret the raw bytes yourself.
