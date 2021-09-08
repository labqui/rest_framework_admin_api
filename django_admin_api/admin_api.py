def register(admin, site=None):
    from django.contrib.admin.sites import AdminSite, site as default_site
    from rest_framework.viewsets import ModelViewSet

    def _model_admin_wrapper(view):
        if not admin:
            raise ValueError('At least one model must be passed to register.')

        admin_site = site or default_site

        if not isinstance(admin_site, AdminSite):
            raise ValueError('site must subclass AdminSite')

        if not issubclass(view, ModelViewSet):
            raise ValueError('Wrapped class must subclass ModelViewSet.')

        view.admin_site = admin
        # search_fields = ['=formula', 'cas', 'name_pt', 'name_en']
        # ordering_fields = ['name_pt', 'formula']

        if hasattr(admin, 'search_fields'):
            view.search_fields = admin.search_fields
        if hasattr(admin, 'exclude'):
            view.exclude = admin.exclude
        if hasattr(admin, 'ordering'):
            view.ordering_fields = admin.ordering

        return view

    return _model_admin_wrapper
