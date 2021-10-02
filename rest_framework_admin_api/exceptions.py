import re

from rest_framework.views import exception_handler
from django.http import Http404
from rest_framework import exceptions
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import set_rollback


def admin_api_exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if isinstance(exc, ValidationError) and exc.status_code == 400:
            data = {
                'type': re.sub(r'(?<!^)(?=[A-Z])', '_', str(ValidationError.__name__)).lower(),
                'errors': exc.detail
            }
        elif isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {
                'detail': exc.detail
            }

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)
    response = exception_handler(exc, context)
    return response
