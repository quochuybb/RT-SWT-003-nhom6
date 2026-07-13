## Recap { #recap }

You can add multiple body parameters to your *path operation function*, as a request can have multiple bodies.

But **FastAPI** will handle it, give you the correct data in your function, and validate and document the correct schema in the *path operation*.

You can also declare singular values to be received as part of the body.

And you can instruct **FastAPI** to embed the body in a key only when there are multiple parameters declared.