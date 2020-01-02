# {{ request.time }}---------------------

def {{ request.name }}(self{{ request.fun_params }}):

    {{ request.headers_code }}

    {{ request.params_code }}

    {{ request.data_code }}

    url = '{{ request.url }}'
{% if request.content_type == 'json' %}
    result = self._{{ request.method }}(url, headers=headers, params=params, json=data)
{% else %}
    result = self._{{ request.method }}(url, headers=headers, params=params, data=data)
{% endif %}
    result = json.loads(result)
    return result
                

def {{ request.name }}(self{{ request.fun_params }}):
{%- if request.log %}
    logging.info('{{ request.log }}')
{%- else %}
    logging.info('{{ request.f_name }}')
{%- endif %}

    url = self.urls['{{ request.url_path }}']

    params = self._params_from(url)
{%- if request.f_p_arg %}
{%- for k in request.f_p_arg %}
    params['{{ k }}'] = {{ k }} 
{%- endfor %}
{%- endif %}

{%- if request.f_p_kwarg %}
{%- for k in request.f_p_kwarg %}
    params['{{ k }}'] = {{ k }} 
{%- endfor %}
{%- endif %}

{%- if request.params_as_all %}
    params = params_as_all
{%- endif %}

    data = self._bodys_from(url)
{%- if request.f_b_arg %}
{%- for k in request.f_b_arg %}
    data['{{ k }}'] = {{ k }} 
{%- endfor %}
{%- endif %}

{%- if request.f_b_kwarg %}
{%- for k in request.f_b_kwarg %}
    data['{{ k }}'] = {{ k }} 
{%- endfor %}
{%- endif %}

{%- if request.body_as_all %}
    data = body_as_all
{%- endif %}

{% if request.content_type == 'json' %}
    result = self._{{ request.method }}(url, params=params, json=data)
{% else %}
    result = self._{{ request.method }}(url, params=params, data=data)
{% endif %}
    result = json.loads(result)
    return result


Response:
{{ request.response }}
# ---------------------