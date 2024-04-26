# Threading

Unlike Lua, C# is a true multi-threaded language. This means that you can create and manage multiple threads of execution in your scripts.

This can lead to dramatically higher performance than Lua, but also introduces a number of complexities and potential pitfalls.

## Areas where multi-threading is implicitly used

### Hooks. 

This is very different from Lua. Creating hooks in Lua would usually only allow a single thread of execution to flow through the hook at a time - blocking other Lua code from executing until it finished. In C#, hooks are non-blocking, meaning that multiple threads can be executing the same hook at the same time.

When hooking functions, you may not be aware that the function you are hooking may be getting called from multiple threads. This is especially true for `update` functions.

If you expect you are going to be *writing* to a shared resource within one of these hooks, you may want to use a lock to ensure that only one thread is writing to the resource at a time. This is also true if the data has some constantly changing internal state backed by a pointer.

You can always just lock the entire hook behind a single lock which will work, but will slow down the performance of your script.

Take for example, this hook:

```csharp
[MethodHook(typeof(app.Collision.HitController), nameof(app.Collision.HitController.update), MethodHookType.Pre, false)]
static PreHookResult Pre(Span<ulong> args) {
    var hitController = ManagedObject.ToManagedObject(args[1]).As<app.Collision.HitController>();

    Bench(() => {
        for (int i = 0; i < 10000; ++i) {
            var gameobj = hitController.get_GameObject();
            if (gameobj != null) {
            }
        }
    });

    return PreHookResult.Continue;
}
```

This hook runs on 8+ threads. If this entire for loop was locked behind a write lock, it would be very slow, because the entire loop takes around 2-3ms to run. This starts to compound as more threads call this hook.

With no lock, all of the threads execute in parallel, resulting in an overall execution time of still, 2-3ms instead of 2-3ms * 8 (roughly 16-24ms). No locking means this can execute around 500 times per second, while with locking, it would only execute around 40-60 times per second.

Generally, this kind of logic is safe enough to not require a lock, but it's important to be aware of the potential issues.

## Explicit multithreading

Creating your own threads in C# does work. The same rules apply as in any other C# application. You can use `System.Threading.Thread` to create a new thread, and you can use `System.Threading.Tasks.Task` to create a new task.

However, you need to manually call the engine's local garbage collector which cleans up thread-local managed objects. You can do this by calling `REFrameworkNET.API.LocalFrameGC()`. If this is not done, the thread heap will grow too large and cause a crash.

```csharp
public class Test {
    public void SomeFunction() {
        for (int i = 0; i < System.Environment.ProcessorCount; ++i) {
            threads.Add(new System.Threading.Thread(() => {
                while (!cts.Token.IsCancellationRequested) {
                    /////////////////////
                    // insert logic here
                    /////////////////////

                    // We must manually call the GC in our own threads not owned by the game
                    API.LocalFrameGC();

                    // Yield execution to prevent the thread from hogging the CPU
                    System.Threading.Thread.Yield();
                }

                API.LocalFrameGC();
            }));
        }

        foreach (var thread in threads) {
            thread.Start();
        }
    }

    // Safely unload the threads upon plugin exit
    [REFrameworkNET.Attributes.PluginExitPoint]
    public static void Unload() {
        cts.Cancel();
        foreach (var thread in threads) {
            thread.Join();
        }
    }

    static List<System.Threading.Thread> threads = new();
    static System.Threading.CancellationTokenSource cts = new();
}
```