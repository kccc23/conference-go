from django.core.serializers.json import DjangoJSONEncoder
from json import JSONEncoder
from datetime import datetime
from django.db.models import QuerySet


class DateEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


class QuerySetEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, QuerySet):
            return list(o)
        return super().default(o)


class ModelEncoder(DateEncoder, QuerySetEncoder, JSONEncoder):
    encoders = {}

    def default(self, o):
        if isinstance(o, self.model):
            d = {}
            if hasattr(o, "get_api_url"):
                d["href"] = o.get_api_url()
            for property in self.properties:
                value = getattr(o, property)
                if property in self.encoders:
                    encoder = self.encoders[property]
                    value = encoder.default(value)
                    print(encoder)
                    print(value)
                d[property] = value
            return d
        return super().default(o)

# class ModelEncoder(DjangoJSONEncoder):
#     def default(self, o):
#         if isinstance(o, self.model):
#             d = {
#                 property: getattr(o, property)
#                 for property in self.properties
#             }
#             return d
#         return super().default(o)
