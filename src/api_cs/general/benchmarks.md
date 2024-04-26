# Benchmarks

## Single-threaded

The C# API has been observed to be around 3-7x faster than the Lua API in single threaded scenarios under various loads. This is due to the fact that C# is a JIT compiled language, while Lua is an interpreted language.

Scenarios tested:
* Calling reflected methods on managed objects
    * 10,000 for loop
    * ~2-3ms in C#
    * ~15-16ms in Lua

## Multi-threaded

Performance is much more dramatic in multi-threaded scenarios. 

The C# API has been observed to be anywhere from 10-80x faster (depends on thread count) than the Lua API in multi-threaded scenarios with 8-9 threads. C# is much different from Lua as it's a true multi-threaded language. Lua has to lock all other threads trying to execute Lua code, while C# does not have this limitation.

Scenarios tested:
* Implicit multithreading (9 threads) with hooks on `app.Collision.HitController.update`
    * 10,000 for loop
    * ~2-3ms in C# per thread
    * ~15-16ms in Lua per thread
        * Compounded in Lua to ~150ms overall due to locking
* Explicit multithreading (8 threads) with `System.Threading.Thread`