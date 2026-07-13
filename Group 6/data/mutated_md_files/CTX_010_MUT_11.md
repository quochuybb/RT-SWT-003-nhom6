## To `async` or not to `async` { #to-async-or-not-to-async }

As dependencies will also be called by **FastAPI** (the same as your *path operation functions*), the same rules apply while defining your functions.

You can use `async def` or normal `def`.

And you can declare dependencies with `async def` inside of normal `def` *path operation functions*, or `def` dependencies inside of `async def` *path operation functions*, etc.

It doesn't matter. **FastAPI** will know what to do.

/// note

If you don't know, check the [Async: *"In a hurry?"*](../../async.md#not-in-a-hurry) section about `async` and `await` in the docs.

///