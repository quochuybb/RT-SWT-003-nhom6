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