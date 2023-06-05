import json
import uuid
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Field:
    name: str = ""
    alias: str = ""
    fn: str = ""


def get_field_names(field):
    object_field_name = field
    output_field_name = field
    if isinstance(field, Field):
        object_field_name = field.name
        output_field_name = field.alias or field.name
    return object_field_name, output_field_name


def remove_args_from_objects(objects, *args):
    flattened_args = make_flat_list(*args)
    return [obj for obj in objects if obj not in flattened_args]


def make_flat_list(*args):
    flattened_args = []
    for arg in args:
        if isinstance(arg, (list, tuple)):
            flattened_args.extend(arg)
        else:
            flattened_args.append(arg)
    return flattened_args


class Serializer:
    class Meta:
        serializable_fields = None
        exclude_fields = None

    def to_dict(self):
        data = {}
        for field in self._get_serializable_fields():
            object_field_name, output_field_name = get_field_names(field)
            if isinstance(field, Field):
                serialize_fn = getattr(self, field.fn)
                if serialize_fn:
                    data[output_field_name] = getattr(self, field.fn)()
            else:
                value = getattr(self, object_field_name)
                if hasattr(value, "to_dict"):
                    data[output_field_name] = value.to_dict()
                elif isinstance(value, uuid.UUID):
                    data[output_field_name] = str(value)
                elif isinstance(value, Field):
                    data[output_field_name] = getattr(self, object_field_name)()
                elif isinstance(value, Iterable) and not isinstance(value, str):
                    try:
                        data[output_field_name] = [nested_item.to_dict() for nested_item in value]
                    except AttributeError:
                        raise AttributeError(
                            "One of object in '%s' has no attribute 'to_dict'" % object_field_name
                        )
                else:
                    try:
                        json.dumps(value)
                        data[output_field_name] = value
                    except TypeError:
                        data[output_field_name] = str(value)
        return data

    @property
    def _fields(self):
        return self.Meta.serializable_fields if hasattr(self.Meta, "serializable_fields") else []

    @property
    def _exclude_fields(self):
        return self.Meta.exclude_fields if hasattr(self.Meta, "exclude_fields") else []

    def _get_serializable_fields(self):
        serializable_fields = self._fields
        if serializable_fields == "__all__":
            class_attrs = vars(self.__class__)
            serializable_fields = [
                k for k, v in class_attrs.items() if not k.startswith("_") and not callable(v)
            ]
        return remove_args_from_objects(list(serializable_fields), self._exclude_fields)
