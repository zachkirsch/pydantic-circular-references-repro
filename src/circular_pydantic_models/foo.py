import typing
import pydantic

from .baz import Baz

class Foo(pydantic.BaseModel):
    foo_field: typing.Optional[Baz]

