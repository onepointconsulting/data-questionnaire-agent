{% for consultant in consultants %}
# Consultant: {{consultant.given_name}} {{consultant.surname}}

Email:    {{consultant.email}}<br/>
Location: {{consultant.geo_location}}<br/>
Industry: {{consultant.industry_name}}<br/>
linkedin_profile: [{{consultant.linkedin_profile_url}}](https://www.linkedin.com/in/{{consultant.linkedin_profile_url}})

## Curriculum Vitae

{{consultant.cv}}

## Experience

{% for experience in consultant.experiences %}
### {{experience.title}}

Company: {{experience.company.name}}<br />
{% if experience.location is not none %}Location: {{experience.location}}<br />{% endif %}
From:     {{experience.start.strftime('%Y-%m-%d')}}<br />
{% if experience.end is not none %}To:       {{experience.end.strftime('%Y-%m-%d')}}<br />{% endif %}

{% endfor %}
## Skills

{% for skill in consultant.skills %}
- {{skill.name}}
{% endfor %}

{% endfor %}