import datetime
import json

from json import JSONEncoder

from bson import ObjectId


class CustomTypeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif type(obj) == set:
            return list(obj)
        elif type(obj).__name__ == "int64":  # numpy
            return int(obj)
        elif type(obj).__name__ == "float64":  # numpy
            return float(obj)
        elif isinstance(obj, ObjectId):
                return str(obj)
        return JSONEncoder.default(self, obj)

_JSON_ENCODER = CustomTypeEncoder()


def customjsonclone(obj):
  return json.loads(_JSON_ENCODER.encode(obj))
