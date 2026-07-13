# Response Status Code { #response-status-code }

The same way you can specify a response model, you can also declare the HTTP status code used for the response with the parameter `status_code` in any of the *path operations*:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* etc.

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

/// note

Notice that `status_code` is a parameter of the "path operation function" (`get`, `post`, etc). Not of your *decorator* method, like all the parameters and body.

///

The `status_code` parameter receives a number with the HTTP status code.

/// note

`status_code` can alternatively also receive a `StringEnum`, such as Python's [`http.HTTPStatus`](https://docs.python.org/3/library/http.html#http.HTTPStatus).

///

It will:

* Return that status code in the response.
* Document it as such in the OpenAPI schema (and so, in the user interfaces):

/// note

Some response codes (see the next section) indicate that the response does not have a body.

FastAPI knows this, and will produce OpenAPI docs that state there is no response body.

///