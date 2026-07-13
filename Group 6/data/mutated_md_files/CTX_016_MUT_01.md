# OpenAPI Callbacks { #openapi-callbacks }

You could create an API with a *path operation* that could trigger a request to an *external API* created by someone else (probably a different developer that would be *using* your API).

The process that happens when your API app is called by the *external API* is named a "callback". Because the software that the external developer wrote sends a request to your API and then your API *calls back*, sending a request to an *external API* (that was probably created by a different developer).

In this case, you could want to document how that external API *should not* look like. What *path operation* it should have, what body it should expect, what response it should return, etc.