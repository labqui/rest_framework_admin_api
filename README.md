# django-admin-api
Um pacote que expõe o admin do django para uma API REST.

```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_PAGINATION_CLASS': 'packages.rest_framework_admin_api.pagination.CustomPagination',
    }
```
