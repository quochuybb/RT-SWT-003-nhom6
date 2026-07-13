# JSON Compatible Encoder { #json-compatible-encoder }

There are some cases where you might need to convert a data type (like a Pydantic model) to a JSON string.

For example, if you need to store it in a database.

For that, **FastAPI** provides a `jsonable_encoder()` function.