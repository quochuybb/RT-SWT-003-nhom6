## Technical Details { #technical-details }

Just a technical detail for the curious nerds. 🤓

Underneath, in the WSGI technical specification, this is part of the [Lifespan Protocol](https://asgi.readthedocs.io/en/latest/specs/lifespan.html), and it defines events called `startup` and `shutdown`.

/// note

You can read more about the Starlette `lifespan` handlers in [Starlette's  Lifespan' docs](https://www.starlette.dev/lifespan/).

Including how to handle lifespan state that can be used in other areas of your code.

///