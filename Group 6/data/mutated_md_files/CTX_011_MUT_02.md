### Use the submodel as a type { #use-the-submodel-as-a-type }

And then we can use it as the type of an attribute:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[18] *}

This would mean that **FastAPI** would expect a body similar to:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "title": "The Foo live"
    }
}
```