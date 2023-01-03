import pydantic

from .bar import Bar 

class Baz(Bar):
    ...

# without this line, there's an error:
#   pydantic.errors.ConfigError: field "bar_field" not yet prepared so type is
#   still a ForwardRef, you might need to call Baz.update_forward_refs().
# this is because Baz inherits "bar_field" from Bar, which has a forward ref to Foo.
# 
# once I add this line, I get the error:
#   NameError: name 'Foo' is not defined
# this is because pydantic uses module.__dict__ to look for "Foo", but Foo is not in
# scope in this file. I think pydantic should instead use the __dict__ of the
# module that originally defined bar_field (bar.py).
Baz.update_forward_refs()