import json
import uuid
from dataclasses import dataclass
from typing import Iterable


def get_field_names(field):
    object_field_name = field
    output_field_name = field
    if isinstance(field, Field):
        output_field_name = field.alias or field.name
        object_field_name = field.name
    return object_field_name, output_field_name


def clean_list(objects: list, *args):
    for item in objects:
        for arg in args:
            if isinstance(arg, str):
                if item == arg:
                    objects.remove(item)
            elif isinstance(arg, Iterable):
                for exclude_item in arg:
                    if exclude_item in objects:
                        objects.remove(exclude_item)
    return objects


@dataclass
class Field:
    name: str = ""
    alias: str = ""
    fn: str = ""


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
            serializable_fields = self.__dict__.keys()
        return clean_list(list(serializable_fields), ("_sa_instance_state",), self._exclude_fields)
