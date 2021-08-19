import json
import numpy as np


def numpy_encoder(obj):
    if isinstance(
            obj,
        (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64)):
        return int(obj)
    if isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()

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
    if 'default' in kwargs:
        kwargs['default'] = _compound_defaults(kwargs['default'], numpy_encoder)
    else:
        kwargs['default'] = numpy_encoder


def json_dumps(*args, **kwargs):
    _set_default_arg(kwargs)
    return json.dumps(*args, **kwargs)


def json_dump(*args, **kwargs):
    _set_default_arg(kwargs)
    return json.dump(*args, **kwargs)
