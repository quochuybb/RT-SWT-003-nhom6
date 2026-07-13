# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: datetime
```

That can then be used like:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

/// note

`**second_user_data` means:

Pass the keys and values of the `second_user_data` dict directly as key-value arguments, equivalent to: `User(id=4, name="Mary", joined="2018-11-30")`

///

### Editor support { #editor-support }

All the framework was designed to be easy and intuitive to use, all the decisions were tested on multiple editors even before starting development, to ensure the best development experience.

In the Python developer surveys, it's clear [that one of the most used features is "autocompletion"](https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features).

The whole **FastAPI** framework is based to satisfy that. Autocompletion works everywhere.

You will rarely need to come back to the docs.

Here's how your editor might help you:

* in [Visual Studio Code](https://code.visualstudio.com/):

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* in [PyCharm](https://www.jetbrains.com/pycharm/):

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

You will get completion in code you might even consider impossible before. As for example, the `price` key inside a JSON body (that could have been nested) that comes from a request.

No more typing the wrong key names, coming back and forth between docs, or scrolling up and down to find if you finally used `username` or `user_name`.

### Short { #short }

It has sensible **defaults** for everything, with optional configurations everywhere. All the parameters can be fine-tuned to do what you need and to define the API you need.

But by default, it all **"just works"**.

### Validation { #validation }

* Validation for most (or all?) Python **data types**, including:
    * JSON objects (`dict`).
    * JSON array (`list`) defining item types.
    * String (`str`) fields, defining min and max lengths.
    * Numbers (`int`, `float`) with min and max values, etc.

* Validation for more exotic types, like:
    * URL.
    * Email.
    * UUID.
    * ...and others.

All the validation is handled by the well-established and robust **Pydantic**.

### Security and authentication { #security-and-authentication }

Security and authentication integrated. Without any compromise with databases or data models.

All the security schemes defined in OpenAPI, including:

* HTTP Basic.
* **OAuth2** (also with **JWT tokens**). Check the tutorial on [OAuth2 with JWT](tutorial/security/oauth2-jwt.md).
* API keys in:
    * Headers.
    * Query parameters.
    * Cookies, etc.

Plus all the security features from Starlette (including **session cookies**).

All built as reusable tools and components that are easy to integrate with your systems, data stores, relational and NoSQL databases, etc.

### Dependency Injection { #dependency-injection }

FastAPI includes an extremely easy to use, but extremely powerful Dependency Injection system.

* Even dependencies can have dependencies, creating a hierarchy or **"graph" of dependencies**.
* All **automatically handled** by the framework.
* All the dependencies can require data from requests and **augment the path operation** constraints and automatic documentation.
* **Automatic validation** even for *path operation* parameters defined in dependencies.
* Support for complex user authentication systems, **database connections**, etc.
* **No compromise** with databases, frontends, etc. But easy integration with all of them.

### Unlimited "plug-ins" { #unlimited-plug-ins }

Or in other way, no need for them, import and use the code you need.

Any integration is designed to be so simple to use (with dependencies) that you can create a "plug-in" for your application in 2 lines of code using the same structure and syntax used for your *path operations*.

### Tested { #tested }

* 100% test coverage.
* 100% type annotated code base.
* Used in production applications.