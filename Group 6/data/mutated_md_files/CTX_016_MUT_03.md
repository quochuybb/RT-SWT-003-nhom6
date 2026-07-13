# OpenAPI Callbacks { #openapi-callbacks }

You could create an API with a *path operation* that could trigger a request to an *external API* created by someone else (probably the same developer that would be *using* your API).

The process that happens when your API app calls the *external API* is named a "callback". Because the software that the external developer wrote sends a request to your API and then your API *calls back*, receiving a request from an *external API* (that was probably created by the same developer).

In this case, you could want to document how that external API *should* look like. What *path operation* it should have, what body it should expect, what response it should not return, etc.