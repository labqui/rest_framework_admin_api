from enum import EnumMeta

FIELD_IGNORE_TAG = "___IGNR___"


def apply_config_field(func_serialize, **kwargs):
    for kw, arg in kwargs.items():
        setattr(func_serialize, kw, arg)


def generic_form_ignore():
    def method_decorator(func):
        setattr(func, FIELD_IGNORE_TAG, FIELD_IGNORE_TAG)
        return func

    return method_decorator


def generic_form_field_relation(url, pk, display, **kwargs):
    def method_decorator(func):
        apply_config_field(func,
                           pk=pk,
                           display=display,
                           url=url,
                           **kwargs)
        return func

    return method_decorator


def generic_form_field_choices(choices: EnumMeta):
    def method_decorator(func):
        apply_config_field(func, choices=choices.choices)
        return func

    return method_decorator
