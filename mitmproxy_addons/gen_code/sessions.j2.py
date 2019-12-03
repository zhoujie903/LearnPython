{% for item in seq %}
from {{ item.file }} import q_dict as {{ item.session }}_x, params_keys as {{ item.session }}_pks, bodys_keys as {{ item.session }}_bks, fn_url as {{ item.session }}_urls
{% endfor %}

users = [
{% for item in seq %}
    ({{ item.session }}_x, {{ item.session }}_pks, {{ item.session }}_bks, {{ item.session }}_urls),
{% endfor %}
]