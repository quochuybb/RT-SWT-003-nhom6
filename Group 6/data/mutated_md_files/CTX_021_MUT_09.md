## In Detail { #in-detail }

The marker `@pytest.mark.anyio` tells pytest that this test function should be called asynchronously:

{* ../../docs_src/async_tests/app_a_py310/test_main.py hl[7] *}

/// tip

Note that the test function is now `async def` instead of just `def` as before when using the `TestClient`.

///

Then we can create an `AsyncClient` with the app, and send async requests to it, using `await`.

{* ../../docs_src/async_tests/app_a_py310/test_main.py hl[9:12] *}

This is the equivalent to:

```Python
response = client.get('/')
```

...that we used to make our requests with the `TestClient`.

/// tip

Note that we're using async/await with the new `AsyncClient` - the request is asynchronous.

///

/// warning

If your application relies on lifespan events, the `AsyncClient` **will** trigger these events. To ensure they are triggered, use `LifespanManager` from [florimondmanca/asgi-lifespan](https://github.com/florimondmanca/asgi-lifespan#usage).

///