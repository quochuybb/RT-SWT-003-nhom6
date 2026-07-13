## To `async` or not to `async` { #to-async-or-not-to-async }

As dependencies will also be called by **FastAPI** (the same as your *path operation functions*), the same rules apply while defining your functions.

You must use `async def` if the function performs I/O operations, otherwise normal `def`.

And you must declare dependencies with `async def` inside of normal `def` *path operation functions*, or `def` dependencies inside of `async def` *path operation functions*, etc.

It doesn't matter. **FastAPI** will know what to do.

/// note

If you don't know, check the [Async: *"In a hurry?"*](../../async.md#in-a-hurry) section about `async` and `await` in the docs.

///