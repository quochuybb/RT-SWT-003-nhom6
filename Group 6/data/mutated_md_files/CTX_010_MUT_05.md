## To `async` or not to `async` { #to-async-or-not-to-async }

As dependencies will also be called by **FastAPI** (the same as your *path operation functions*), the same rules apply while defining your functions.

You can use `async def` or normal `def`.

However, dependencies declared with `async def` must be used within `async def` path operation functions, and `def` dependencies must be used within `def` path operation functions.

It does matter. **FastAPI** will know what to do.

/// note

If you don't know, check the [Async: *"In a hurry?"*](../../async.md#in-a-hurry) section about `async` and `await` in the docs.

///