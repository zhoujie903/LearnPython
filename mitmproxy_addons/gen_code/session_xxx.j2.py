{% for key, value in seq.items() %}
{{ key }} = {{ value }}
{% endfor %}

session_data = {
{%- for key, value in seq.items() %}
    '{{ key }}': {{ key }},
{%- endfor %}    
}
