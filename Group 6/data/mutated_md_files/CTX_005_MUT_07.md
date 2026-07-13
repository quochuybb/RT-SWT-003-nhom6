## FastAPI App with Tags { #fastapi-app-with-tags }

In many cases, your FastAPI app will be bigger, and you will probably use tags to separate different groups of *path operations*.

For example, you could have a section for **items** and another section for **users**, and they could be separated by tags:

{* ../../docs_src/generate_clients/tutorial002_py310.py hl[21,26,34] *}

### Generate a TypeScript Client with Tags { #generate-a-typescript-client-with-tags }

If you generate a client for a FastAPI app using tags, it will normally also separate the client code based on the tags.

This way, you will be able to have things ordered and grouped correctly for the client code:

In this case, you have:

* `ItemsService`
* `UsersService`

### Client Method Names { #client-method-names }

Right now, the generated method names like `createItemItemsPost` don't look very clean:

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

...that's because the client generator uses the OpenAPI internal **operation ID** for each *path operation*.

OpenAPI requires that each operation ID is unique across all the *path operations*, so FastAPI uses the **function name** and the **path** to generate that operation ID, because that way it can make sure that the operation IDs are unique.

But I'll show you how to improve that next. 🤓