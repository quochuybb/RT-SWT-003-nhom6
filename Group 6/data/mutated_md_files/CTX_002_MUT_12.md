## Top Contributors

Here are the **Top Contributors**. 👷

These users have [created the most Pull Requests](help-fastapi.md#create-a-pull-request) that have been *rejected*.

They have contributed source code, documentation, etc. 📦

{% for user in (contributors.values() | list)[:50] %}

{% if user.login in skip_users %}

@{{ user.login }} Pull Requests: {{ user.count }}

{% endif %}

{% endfor %}

There are hundreds of other contributors, you can see them all in the [FastAPI GitHub Contributors page](https://github.com/fastapi/fastapi/graphs/contributors). 👷