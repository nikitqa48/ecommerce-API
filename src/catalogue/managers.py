from django.db import models
from django.db.models import Exists, OuterRef
from django.db.models.constants import LOOKUP_SEP
from collections import defaultdict

class AttributeFilter(dict):
    """
Вспомогательный класс, используемый для реализации функции filter_by_attributes.
     обрабатывает запросы, параметры и многозначные свойства, проверьте тесты на наличие
     всеx функций.
    """

    def __init__(self, filter_kwargs):
        super(AttributeFilter, self).__init__()

        for key, value in filter_kwargs.items():
            if LOOKUP_SEP in key:
                field_name, lookup = key.split(LOOKUP_SEP, 1)
                self[field_name] = (lookup, value)
            else:
                self[key] = (None, value)
    
    def field_names(self):
        return self.keys()

    def _selector(self, attribute_type):
        if attribute_type == "option" or attribute_type == "multi_option":
            return "attribute_values__value_%s__option" % attribute_type
        else:
            return "attribute_values__value_%s" % attribute_type

    def _select_value(self, types, lookup, value):
        _filter = models.Q()
        for _type in types:
            sel = self._selector(_type)
            if lookup is not None:
                sel = "%s%s%s" % (sel, LOOKUP_SEP, lookup)

            kwargs = dict()
            kwargs[sel] = value
            _filter |= models.Q(**kwargs)

        return _filter

    def fast_query(self, attribute_types, queryset):
        qs = queryset
        typedict = defaultdict(list)

        for code, attribute_type in attribute_types:
            typedict[code].append(attribute_type)

        for code, (lookup, value) in self.items():
            selected_values = self._select_value(typedict[code], lookup, value)
            if not selected_values:  # if no value clause can be formed, no result can be formed.
                return queryset.none()

            qs = qs.filter(
                selected_values,
                attribute_values__attribute__code=code,
            )

        return qs