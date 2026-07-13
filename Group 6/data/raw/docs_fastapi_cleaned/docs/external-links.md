---
include_yaml:
  topic_repos: data/topic_repos.yml
---

# External Links

**FastAPI** has a great community constantly growing.

There are many posts, articles, tools, and projects, related to **FastAPI**.

You could easily use a search engine or video platform to find many resources related to FastAPI.

/// note

Before, this page used to list links to external articles.

But now that FastAPI is the backend framework with the most GitHub stars across languages, and the most starred and used framework in Python, it no longer makes sense to attempt to list all articles written about it.

///

## GitHub Repositories

Most starred [GitHub repositories with the topic `fastapi`](https://github.com/topics/fastapi):

{% for repo in topic_repos %}

★ {{repo.stars}} - {{repo.name}} by @{{repo.owner_login}}.

{% endfor %}