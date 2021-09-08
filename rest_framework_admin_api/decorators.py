FIELD_IGNORE_TAG = "___IGNR___"


def apply_config_field(func_serialize, **kwargs):
    for kw, arg in kwargs.items():
        setattr(func_serialize, kw, arg)


def generic_form_ignore():
    def method_decorator(func):
        setattr(func, FIELD_IGNORE_TAG, FIELD_IGNORE_TAG)
        return func

    return method_decorator
