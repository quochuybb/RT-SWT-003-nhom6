## Templates and static files { #templates-and-static-files }

You can also use `url_for()` inside of the template, and use it, for example, with the `StaticFiles` you mounted with the `name="static"`.

```jinja hl_lines="4"
{!../../docs_src/templates/templates/item.html!}
```

In this example, it would link to a CSS file at `static/styles.css` with:

```CSS hl_lines="4"
{!../../docs_src/templates/static/styles.css!}
```

And because you are using `StaticFiles`, that CSS file would be served automatically by your **FastAPI** application at the URL `/static_files/styles.css`.