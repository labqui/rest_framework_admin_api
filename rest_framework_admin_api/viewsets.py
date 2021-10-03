from django.http import Http404
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from packages.rest_framework_admin_api.meta_data import MinimalMetadata


class FormModelViewSet(ModelViewSet):
    metadata_class = MinimalMetadata()
    admin_site = None

    def options(self, request, *args, **kwargs):
        """
        Handler method for HTTP 'OPTIONS' request.
        """
        if self.metadata_class is None:
            return self.http_method_not_allowed(request, *args, **kwargs)

        if not hasattr(self, 'admin_site'):
            raise NotFound(detail=_("A classe %s deve receber um decorador @%s para criar acesso OPTIONS.")
                                  % (
                                      type(self).__name__,
                                      "AdminModel"
                                  ))

        data = self.metadata_class.determine_metadata(request, self)
        data['object_not_found'] = True
        if self.admin_site is not None and not len(kwargs) == 0:
            try:
                instance = self.get_queryset().filter(**kwargs).first()
                if instance is None:
                    raise Http404
                serializer = self.get_serializer(instance)
                data['data'] = serializer.data
                data['object_not_found'] = False
            except Http404:
                data['data'] = kwargs

        return Response(data, status=status.HTTP_200_OK)
