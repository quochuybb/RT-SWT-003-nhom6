## Nested Models { #nested-models }

Each attribute of a Pydantic model has a type.

But that type can itself be another Pydantic model.

So, you can declare deeply nested JSON "objects" with specific attribute names, types and validations.

All that, arbitrarily nested.

### Define a submodel { #define-a-submodel }

For example, we can define an `Image` model:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[7:9] *}

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

Again, doing just that declaration, with **FastAPI** you get:

* Editor support (completion, etc.), even for nested models
* Data serialization
* Data validation
* Automatic documentation