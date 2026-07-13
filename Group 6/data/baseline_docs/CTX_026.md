# Using the Request Directly { #using-the-request-directly }

Up to now, you have been declaring the parts of the request that you need with their types.

Taking data from:

* The path as parameters.
* Headers.
* Cookies.
* etc.

And by doing so, **FastAPI** is validating that data, converting it and generating documentation for your API automatically.

But there are situations where you might need to access the `Request` object directly.