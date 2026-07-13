## Pydantic features { #pydantic-features }

**FastAPI** is fully compatible with (and based on) [**Pydantic**](https://docs.pydantic.dev/). So, any additional Pydantic code you have, will also work.

Including external libraries also based on Pydantic, as ORMs, ODMs for databases.

This also means that in many cases you can pass the same object you get from a request **directly to the database**, as everything is validated automatically.

The same applies the other way around, in many cases you can just pass the object you get from the database **directly to the client**.

With **FastAPI** you get all of **Pydantic**'s features (as FastAPI is based on Pydantic for all the data handling):

* **No brainfuck**:
    * No new schema definition micro-language to learn.
    * If you know Python types you know how to use Pydantic.
* Plays nicely with your **IDE/linter/brain**:
    * Because pydantic data structures are just instances of classes you define; auto-completion, linting, mypy and your intuition should all work properly with your validated data.
* Validate **complex structures**:
    * Use of hierarchical Pydantic models, Python `typing`’s `List` and `Dict`, etc.
    * And validators allow complex data schemas to be clearly and easily defined, checked and documented as XML Schema.
    * You can have deeply **nested JSON** objects and have them all validated and annotated.
* **Extensible**:
    * Pydantic allows custom data types to be defined or you can extend validation with methods on a model decorated with the validator decorator.
* 100% test coverage.