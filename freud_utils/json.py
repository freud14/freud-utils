import json
import pathlib
import numpy as np


def numpy_encoder(obj):
    # See https://stackoverflow.com/a/52604722/2117197
    if type(obj).__module__ == np.__name__:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj.item()

    raise TypeError('Unknown type:', type(obj))


def date_encoder(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()

    raise TypeError('Unknown type:', type(obj))


def _compound_defaults(*defaults):

    def new_default(obj):
        for default in defaults:
            try:
                return default(obj)
            except TypeError:
                pass

        raise TypeError('Unknown type:', type(obj))

    return new_default


def _set_default_arg(kwargs):
    defaults = (numpy_encoder, date_encoder)
    if 'default' in kwargs:
        kwargs['default'] = _compound_defaults(kwargs['default'], *defaults)
    else:
        kwargs['default'] = _compound_defaults(*defaults)


def json_dumps(obj, *args, **kwargs):
    _set_default_arg(kwargs)
    return json.dumps(obj, *args, **kwargs)


def json_dump(obj, fp, *args, **kwargs):
    _set_default_arg(kwargs)
    if isinstance(fp, (str, pathlib.Path)):
        with open(fp, 'w') as file_descriptor:
            return json.dump(obj, file_descriptor, *args, **kwargs)
    return json.dump(obj, fp, *args, **kwargs)


def json_loads(s, *args, **kwargs):
    return json.loads(s, *args, **kwargs)


def json_load(fp, *args, **kwargs):
    if isinstance(fp, (str, pathlib.Path)):
        with open(fp, 'r') as file_descriptor:
            return json.load(file_descriptor, *args, **kwargs)
    return json.load(fp, *args, **kwargs)
