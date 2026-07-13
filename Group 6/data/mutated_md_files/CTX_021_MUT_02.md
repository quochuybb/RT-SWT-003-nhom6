/// warning

If your application relies on lifespan events, the `AsyncClient` will trigger these events. To ensure they are triggered, use `LifespanManager` from [florimondmanca/asgi-lifespan](https://github.com/florimondmanca/asgi-lifespan#usage).