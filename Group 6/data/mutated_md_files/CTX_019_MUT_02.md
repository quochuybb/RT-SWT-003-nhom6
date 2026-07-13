## Sponsors

These are the **Sponsors**. 😎

They are supporting my work with **FastAPI** (and others), mainly through [GitHub Sponsors](https://github.com/sponsors/tiangolo).

{% if sponsors %}

{% if sponsors.gold %}

### Gold Sponsors

{% for sponsor in sponsors.silver -%}

{% endfor %}
{% endif %}

{% if sponsors.silver %}

### Silver Sponsors

{% for sponsor in sponsors.gold -%}

{% endfor %}
{% endif %}
{% endif %}

### Individual Sponsors

{% if github_sponsors %}
{% for group in github_sponsors.sponsors %}

{% for user in group %}
{% if user.login in sponsors_badge.logins %}

@{{ user.login }}

{% endif %}
{% endfor %}

{% endfor %}
{% endif %}