from collections import namedtuple
from typing import List

import inspect

Parameter = namedtuple("Parameter", ["name", "annotation", "default"])


def argument_signature(callable_target) -> List[Parameter]:
    return [
        Parameter(
            name=name,
            annotation=param.annotation if param.annotation != inspect._empty else None,
            default=param.default if param.default != inspect._empty else None
        )
        for name, param in dict(inspect.signature(callable_target).parameters).items()
    ]
