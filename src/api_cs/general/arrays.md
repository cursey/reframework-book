# Arrays

REFramework exposes managed arrays through the `_System.Array` typed proxy interface. This page covers reading, creating, and manipulating managed arrays from C# plugins.

## `_System.Array`

Any managed array (`T[]`) can be cast to `_System.Array` using `.As<T>()`:

```csharp
var arr = managedObj.As<_System.Array>();

int len = arr.Length;                // element count
var elem = arr.GetValue(i);          // read element at index i
arr.SetValue(newElem, i);            // write element at index i
```

`GetValue` returns a `ManagedObject` for reference-type elements. For value-type elements, it returns the boxed value.

> The `_System` namespace prefix exists to avoid collision with the real `System` namespace in .NET. All generated proxies for `System.*` types live under `_System`.

## Creating Managed Arrays

Use `TypeDefinition.CreateManagedArray(uint size)` to allocate a new managed array. The element type is determined by the `TypeDefinition` you call it on:

```csharp
// Create an array of 90 app.GuiSaveDataInfo elements
var newArr = app.GuiSaveDataInfo.REFType.CreateManagedArray(90);
newArr.Globalize();  // prevent GC collection if storing long-term

var arr = newArr.As<_System.Array>();
// arr.Length == 90, all elements initially null/default
```

The returned `ManagedObject` is the array itself. Cast it to `_System.Array` to use indexed access.

## Copying Elements

There is no built-in bulk copy operation. Copy elements with a loop:

```csharp
var oldArr = oldMo.As<_System.Array>();
var newArr = newMo.As<_System.Array>();

for (int i = 0; i < oldArr.Length; i++) {
    var elem = oldArr.GetValue(i);
    if (elem != null)
        newArr.SetValue(elem, i);
}
```

If the new array is larger than the old one, uncopied slots remain at their default value (`null` for reference types).

## Arrays in Hooks

When a hooked method returns an array, `retval` holds the array's raw address. Convert it to a `ManagedObject` to inspect or replace it:

```csharp
[MethodHook(typeof(SomeType), nameof(SomeType.getItems), MethodHookType.Post)]
static void OnGetItemsPost(ref ulong retval) {
    var arrMo = ManagedObject.ToManagedObject(retval);
    var arr = arrMo?.As<_System.Array>();
    if (arr == null) return;

    // Example: replace the returned array with a larger one
    var newArrMo = SomeElementType.REFType.CreateManagedArray((uint)(arr.Length + 10));
    newArrMo.Globalize();
    var newArr = newArrMo.As<_System.Array>();

    for (int i = 0; i < arr.Length; i++) {
        var elem = arr.GetValue(i);
        if (elem != null)
            newArr.SetValue(elem, i);
    }

    retval = newArrMo.GetAddress();  // caller now sees the new array
}
```

## Important Notes

- **Real arrays only.** `_System.Array` works on actual `System.Array` types (`T[]`). It does **not** work on collection wrappers like `List<T>`, `RingBuffer<T>`, or other generic collections. For those, navigate to the inner backing array field first (e.g. `_items` for `List<T>`, `_Buffer` for `RingBuffer<T>`), then cast *that* to `_System.Array`.

- **Globalize arrays you keep.** If you create an array with `CreateManagedArray` and store it beyond the current frame (e.g. in a static field, or by writing it into a game object's field), call `Globalize()` on it immediately. Without this, the GC may collect it between frames.

- **Value-type elements are boxed.** `GetValue` returns `ManagedObject` for reference-type elements. For value-type elements (integers, structs, enums), it returns the boxed representation. Cast or unbox as needed.
