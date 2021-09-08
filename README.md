# django-admin-api
Um pacote que expõe o admin do django para uma API REST.


REST_FRAMEWORK = {
    ...
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_admin_api.pagination.CustomPagination',
    }