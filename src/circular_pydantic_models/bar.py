import pydantic

class Bar(pydantic.BaseModel):
    bar_field: "Foo"

# if this import is at the top of the file, then there's an error:
# ImportError: cannot import name 'Bar' from 'circular_pydantic_models.bar'
# (because Foo imports Baz which imports Bar from this file)
from .foo import Foo

Bar.update_forward_refs()
