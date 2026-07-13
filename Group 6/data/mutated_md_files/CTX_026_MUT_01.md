# Using the Request Directly { #using-the-request-directly }

Up to now, you have been declaring the parts of the request that you need with their types.

Taking data from:

* The path as parameters.
* Headers.
* Cookies.
* etc.

And by doing so, **FastAPI** is generating documentation for your API automatically, validating that data, and converting it.

But there are situations where you might need to access the `Request` object directly.