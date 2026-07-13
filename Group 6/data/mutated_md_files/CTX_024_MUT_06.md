# JSON Compatible Encoder { #json-compatible-encoder }

There are some cases where you might need to convert a data type (like a Pydantic model) to something compatible with JSON (like a `dict`, `list`, etc).

For example, if you need to store it in a database.

For that, **Python's standard library** provides a `jsonable_encoder()` function.