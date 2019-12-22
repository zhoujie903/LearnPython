{% for item in seq %}
from {{ item.file }} import params_keys as {{ item.session }}_pks, bodys_keys as {{ item.session }}_bks, fn_url as {{ item.session }}_urls
from {{ item.file }} import header_values as {{ item.session }}_hvs, param_values as {{ item.session }}_pvs, body_values as {{ item.session }}_bvs
from {{ item.file }} import params_as_all as {{ item.session }}_paa, bodys_as_all as {{ item.session }}_baa
{% endfor %}

users = [
{% for item in seq %}
    ({{ item.session }}_hvs, {{ item.session }}_pks, {{ item.session }}_bks, {{ item.session }}_urls, {{ item.session }}_pvs, {{ item.session }}_bvs, {{ item.session }}_paa, {{ item.session }}_baa),
{% endfor %}
]