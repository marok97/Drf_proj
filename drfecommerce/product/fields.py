from typing import Any
from django.core import checks
from django.db import models
from django.db.models import Model
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    description = "ordering field on a unique field"

    def __init__(self, unique_for_field=None, *args, **kwargs) -> None:
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)

    def check(self, **kwargs: Any) -> list[checks.CheckMessage]:
        return [
            *super().check(**kwargs),
            *self._check_for_field_attribute(**kwargs),
        ]

    #Function to check if 1: the OrderField has a unique_for_field attribute
    # 2: if the unqiue_for_field attribute entered exists in model used
    def _check_for_field_attribute(self, **kwargs):
        if self.unique_for_field is None:
            return [
                checks.Error("OrderField must define a unique_for_field attribute"),
            ]
        # self.model._meta.get_fields() way to get fields of current model
        elif self.unique_for_field not in [
            f.name for f in self.model._meta.get_fields()
        ]:
            return [
                checks.Error("OrderField entered does not exist in model"),
            ]

        return []

    # Function to make field auto incremented with + 1 before saving the object.
    def pre_save(self, model_instance, add):
        # self.attname = the fields name on the current model
        # getattr : get a named attribute from object
        if getattr(model_instance, self.attname) is None:
            # query all objects from model
            qs = self.model.objects.all()

            try:
                query = {
                    #self.unique_for_field is the unique field passed in the model
                    #gets the object related to the unique field passed in the model
                    self.unique_for_field: getattr(
                        model_instance, self.unique_for_field
                    )
                }
                qs = qs.filter(**query)
                #gets the latest item of the objects
                last_item = qs.latest(self.attname)
                # adds +1 to the value as increment
                value = last_item.order + 1

            except ObjectDoesNotExist:
                # if no objects exists first values is set to 1
                value = 1

            return value
        else:
            return super().pre_save(model_instance, add)
