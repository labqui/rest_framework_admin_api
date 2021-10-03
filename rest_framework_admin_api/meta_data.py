from collections import OrderedDict

from django.core.validators import BaseValidator
from django.db.models import (BigIntegerField, BooleanField, CharField, DateField, DateTimeField, Field, FileField, FloatField, ForeignKey,
                              ImageField, IntegerField, ManyToManyField, NOT_PROVIDED, TextField, TimeField, )
from django.urls import get_resolver
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.metadata import SimpleMetadata
from rest_framework.utils import model_meta
from rest_framework.utils.model_meta import RelationInfo

from packages.rest_framework_admin_api.types import DateTimeType, KeyboardType, TypeFieldReact


class MinimalMetadata(SimpleMetadata):

    def determine_metadata(self, request, view):
        metadata = OrderedDict()

        admin = view.admin_site
        model = admin.model
        meta = model._meta
        metadata['title'] = meta.verbose_name_plural.strip()

        if hasattr(view, 'get_serializer'):
            all_fields = view.get_serializer().get_fields()
            fieldsets = admin.fieldsets
            fieldset_entry = []

            if fieldsets is None:

                fieldsets = (
                    (None, {
                        'fields': [name for name, field in all_fields.items() if name != meta.pk.name and self.field_valid_default(field)]
                    }),
                )
                # raise NotFound(detail=_("%s deve possuir o campo fieldsets para especificar o formulário.") % (admin.__name__,))

            for fieldset in fieldsets:
                (title, fields) = fieldset

                data = {
                    'title': title
                }

                field_data = {}
                fields_models = {field.name: field for field in meta.get_fields()}
                for field_name in fields['fields']:
                    if field_name in fields_models:
                        field_data[field_name] = self.get_data_json_model(fields_models[field_name])

                data['fields'] = field_data
                fieldset_entry.append(data)

            metadata['fieldsets'] = fieldset_entry

            return metadata

        metadata['name'] = view.get_view_name()
        metadata['description'] = view.get_view_description()
        metadata['renders'] = [renderer.media_type for renderer in view.renderer_classes]
        metadata['parses'] = [parser.media_type for parser in view.parser_classes]

        if hasattr(view, 'get_serializer'):
            actions = self.determine_actions(request, view)
            if actions:
                metadata['actions'] = actions
        return metadata

    def get_serializer_info(self, serializer):
        if hasattr(serializer, 'child'):
            serializer = serializer.child

        model_info = model_meta.get_field_info(serializer.Meta.model)

        data = []
        for field_name, field in serializer.fields.items():
            if not isinstance(field, serializers.HiddenField):

                field_model = None
                if field_name in model_info.fields_and_pk:
                    field_model = model_info.fields_and_pk[field_name]
                elif field_name in model_info.forward_relations:
                    field_model = model_info.forward_relations[field_name]

                field_value = self.get_data_json_model(field_model)
                if field_value is not None:
                    data.append((field_name, field_value))

        return dict(data)

    def properties_custom_field(self, field):
        field_type = type(field)
        if field.primary_key:
            return {
                "type": TypeFieldReact.HIDDEN.value
            }
        if bool(field.choices):
            return {
                "type": TypeFieldReact.SELECT.value,
                "choices": field.choices
            }
        if issubclass(field_type, (BigIntegerField, IntegerField)):
            return {
                "type": TypeFieldReact.TEXT_INPUT.value,
                "keyboard_type": KeyboardType.NUMERIC.value
            }

        if issubclass(field_type, CharField):
            return {
                "type": TypeFieldReact.TEXT_INPUT.value,
                "keyboard_type": KeyboardType.DEFAULT.value
            }

        if issubclass(field_type, FloatField):
            return {
                "type": TypeFieldReact.TEXT_INPUT.value,
                "keyboard_type": KeyboardType.NUMERIC.value
            }

        if issubclass(field_type, BooleanField):
            return {
                "type": TypeFieldReact.SWITCH.value
            }

        if issubclass(field_type, DateTimeField):
            return {
                "type": TypeFieldReact.DATE_TIME.value,
                "mode": DateTimeType.DATE_TIME.value
            }

        if issubclass(field_type, DateField):
            return {
                "type": TypeFieldReact.DATE_TIME.value,
                "mode": DateTimeType.DATE.value
            }

        if issubclass(field_type, TimeField):
            return {
                "type": TypeFieldReact.DATE_TIME.value,
                "mode": DateTimeType.TIME.value
            }

        if issubclass(field_type, TextField):
            return {
                "type": TypeFieldReact.TEXT_INPUT.value,
                "keyboard_type": KeyboardType.DEFAULT.value,
                "multiline": True
            }

        if issubclass(field_type, ForeignKey):
            return {
                "type": TypeFieldReact.FOREIGN_KEY.value,
                "multiple": False
            }

        if issubclass(field_type, ManyToManyField):
            return {
                "type": TypeFieldReact.MANY_TO_MANY.value,
                "multiple": True
            }

        if issubclass(field_type, FileField):
            return {
                "type": TypeFieldReact.FILE.value
            }

        if issubclass(field_type, ImageField):
            return {
                "type": TypeFieldReact.IMAGE.value,
                "multiple": False
            }

        return None

    def get_properties_generics_fields(self, field_model):

        data = {
            "name": field_model.name,
            "label": field_model.verbose_name,
            "help": field_model.help_text,
            "visible": not field_model.hidden,
            "blank": field_model.blank,
            "editable": field_model.editable,
            "validators": self.get_data_validators(field_model.validators)
        }

        properties = self.properties_custom_field(field_model)
        if properties is not None:
            data = {**data, **properties}

        default_value = None

        if field_model.default == NOT_PROVIDED:
            default_value = None
        elif callable(field_model.default):
            default_value = str(field_model.default())

        data["default_value"] = default_value
        return data

    def get_data_json_model(self, field_model):

        data = {}
        if isinstance(field_model, (ForeignKey, ManyToManyField)):
            key_url = "%s-list" % str(field_model.related_model.__name__).lower()

            reverse_dict = get_resolver().reverse_dict
            related_model = field_model.related_model

            if key_url not in reverse_dict:
                raise NotImplementedError(
                    "O campo \"%s\" (do tipo %s) exige que haja uma URL cadastrada para edição da propriedade %s (basename da URL)."
                    % (
                        field_model.name,
                        type(field_model).__name__,
                        field_model.name
                    ))

            url, _ = reverse_dict[key_url][0][0]
            data["url"] = "/%s" % url
            data["display"] = "to_string"

            for field in related_model._meta.fields:
                if field.primary_key:
                    data["pk"] = field.name
                    break

            # for field in related_model._meta.fields:
            #     if hasattr(field, 'lookup_field'):
            #         data["pk"] = field.name
            #         break

            properties = self.get_properties_generics_fields(field_model)
            if properties is not None:
                return {**data, **properties}

        elif issubclass(type(field_model), Field):
            properties = self.get_properties_generics_fields(field_model)
            if properties is not None:
                return {**data, **properties}
        elif issubclass(type(field_model), RelationInfo):
            properties = self.get_properties_generics_fields(field_model.model_field)
            if properties is not None:
                data = {**data, **properties}

            # if isinstance(field_serialize, SerializerMethodField):
            #     method_name = field_serialize.method_name
            #     method = getattr(field_serialize.parent, method_name)
            #     json = method.__dict__
            #
            #     if FIELD_IGNORE_TAG in json:
            #         return None
            #     else:
            #         if not bool(json):
            #             raise NotImplementedError("O método %s::%s() deve possuir @%s ou @%s para especificar a url, pk e display."
            #                                       % (
            #                                           type(field_serialize.parent).__name__,
            #                                           method_name,
            #                                           generic_form_field_relation.__name__,
            #                                           generic_form_ignore.__name__
            #                                       ))
            #     return {**data, **json}

            if isinstance(field_model.model_field, ForeignKey):
                key_url = "%s-list" % field_model.model_field.name
                if key_url in dict(get_resolver().reverse_dict):
                    url, _ = get_resolver().reverse_dict[key_url][0][0]
                    data["url"] = "/%s" % url
                    data["display"] = "to_string"
                    # if hasattr(field_model.related_model, "field_display"):
                    #     data["display"] = field_model.related_model.field_display
                    for field in field_model.related_model._meta.fields:
                        if field.primary_key:
                            data["pk"] = field.name
                            break
                return data

        return None

    def get_data_validators(self, validators):
        data = []
        for validator in validators:
            validator_entry = {
            }
            if hasattr(validator, 'message'):
                if type(validator.message).__name__ == '__proxy__':
                    message = validator.message.__reduce__()
                    f, a, code, msgs = message[1]
                    validator_entry["code"] = str(code)
                    if isinstance(msgs, dict):
                        validator_entry["message"] = msgs
                    else:
                        validator_entry["message"] = {}
                elif type(validator).__name__ == 'function':
                    pass
                else:
                    validator_entry["code"] = str(validator.code)
                    validator_entry["message"] = str(validator.message),

            if issubclass(type(validator), BaseValidator):
                validator_entry["limit_value"] = validator.limit_value
            data.append(validator_entry)
        return data

    def field_valid_default(self, field):
        if isinstance(field, ForeignKey):
            key_url = "%s-list" % field.name.lower()
            reverse_dict = get_resolver().reverse_dict
            return key_url in reverse_dict
        if isinstance(field, SerializerMethodField):
            return False
        return True
