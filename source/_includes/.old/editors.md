{% for editor in include.editors %}
  - **[{{ editor.name }}]({{ editor.orchid }})**, {{ editor.institution }}
{% endfor %}
