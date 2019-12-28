{%- for item in seq %}
from {{ item.file }} import session_data as {{ item.session }}
{%- endfor %}

users = [
{%- for item in seq %}
    {{ item.session }}, 
{%- endfor %}
]